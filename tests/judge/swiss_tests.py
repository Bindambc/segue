import mockito

from .service_tests import JudgeTestCases

from ..support import hashie
from ..support.factories import *
from segue.judge.errors import *
from segue.judge.swiss import TrivialRoundGenerator, ClassicalRoundGenerator, StandingsCalculator, Player

class TrivialRoundGeneratorTestCases(JudgeTestCases):
    def setUp(self):
        super(TrivialRoundGeneratorTestCases, self).setUp()
        self.generator = TrivialRoundGenerator()

    def test_pairs_players_two_by_two(self):
        ctx = self.setUpProposals()

        ordered_players  = [ Player(p,0) for p in [ctx.p1,ctx.p2,ctx.p3,ctx.p4,ctx.p5,ctx.p6]]
        past_matches = []

        result = self.generator.generate(ordered_players, past_matches, round=1)

        self.assertEquals(len(result), 3)
        self.assertEquals([ x.round for x in result ], [1,1,1])
        self.assertEquals(result[0].player1, ctx.p1)
        self.assertEquals(result[0].player2, ctx.p2)
        self.assertEquals(result[1].player1, ctx.p3)
        self.assertEquals(result[1].player2, ctx.p4)
        self.assertEquals(result[2].player1, ctx.p5)
        self.assertEquals(result[2].player2, ctx.p6)

    def test_pairs_odd_player_as_a_bye(self):
        ctx = self.setUpProposals()
        p7 = self.create_from_factory(ValidProposalFactory, id=7, title='bye bye')
        ordered_players  = [ Player(p,0) for p in [ctx.p1,ctx.p2,ctx.p3,ctx.p4,ctx.p5,ctx.p6,p7]]
        past_matches = []

        result = self.generator.generate(ordered_players, past_matches, round=1)

        self.assertEquals(len(result), 4)
        self.assertEquals(result[3].player1, p7)
        self.assertEquals(result[3].player2, None)
        self.assertEquals(result[3].result, 'player1')

class ClassicalRoundGeneratorTestCases(JudgeTestCases):
    def setUp(self):
        super(ClassicalRoundGeneratorTestCases, self).setUp()
        self.generator = ClassicalRoundGenerator()

    def test_does_not_generate_a_new_round_if_there_is_one_ongoing(self):
        ctx = self.setUpProposals()
        ctx = self.setUpExistingRoundWithPendingMatches(ctx)

        ordered_players  = [ Player(p,0) for p in [ctx.p1,ctx.p6,ctx.p3,ctx.p4,ctx.p2,ctx.p5]]
        past_matches = [ctx.m1,ctx.m2,ctx.m3]

        with self.assertRaises(RoundHasPendingMatches):
            result = self.generator.generate(ordered_players, past_matches, 2)

    def test_does_not_repeat_already_existing_match(self):
        ctx = self.setUpProposals()
        ctx = self.setUpExistingMatches(ctx)

        ordered_players  = [ Player(p,0) for p in [ctx.p1,ctx.p6,ctx.p3,ctx.p4,ctx.p2,ctx.p5]]
        past_matches = [ctx.m1,ctx.m2,ctx.m3]

        result = self.generator.generate(ordered_players, past_matches, 2)
        self.assertEquals(result[0].player1, ctx.p1)
        self.assertEquals(result[0].player2, ctx.p6)
        self.assertEquals(result[1].player1, ctx.p3)
        self.assertEquals(result[1].player2, ctx.p2)
        self.assertEquals(result[2].player1, ctx.p4)
        self.assertEquals(result[2].player2, ctx.p5)

    def test_pairs_odd_player_as_a_bye(self):
        ctx = self.setUpProposals()
        p7 = self.create_from_factory(ValidProposalFactory, id=7, title='bye bye')
        ordered_players  = [ Player(p,0) for p in [ctx.p1,ctx.p2,ctx.p3,ctx.p4,ctx.p5,ctx.p6,p7]]
        past_matches = []

        result = self.generator.generate(ordered_players, past_matches, round=1)

        self.assertEquals(len(result), 4)
        self.assertEquals(result[3].player1, p7)
        self.assertEquals(result[3].player2, None)
        self.assertEquals(result[3].result, 'player1')

class StandingsCalculatorTestCases(JudgeTestCases):
    def setUp(self):
        super(StandingsCalculatorTestCases, self).setUp()
        self.calculator = StandingsCalculator()

    def test_sorts_by_number_of_points(self):
        ctx = self.setUpProposals()
        ctx = self.setUpExistingMatches(ctx)

        proposals = [ctx.p1,ctx.p2,ctx.p3,ctx.p4,ctx.p5,ctx.p6]
        past_matches = [ctx.m1,ctx.m2,ctx.m3]

        mockito.when(ctx.m1).result_for(ctx.p1).thenReturn('victory')
        mockito.when(ctx.m1).result_for(ctx.p2).thenReturn('defeat')
        mockito.when(ctx.m2).result_for(ctx.p3).thenReturn('tie')
        mockito.when(ctx.m2).result_for(ctx.p4).thenReturn('tie')
        mockito.when(ctx.m3).result_for(ctx.p5).thenReturn('defeat')
        mockito.when(ctx.m3).result_for(ctx.p6).thenReturn('victory')

        result = self.calculator.calculate(proposals, past_matches)

        self.assertEquals([ p.position for p in result ], [ 1, 2, 3, 4, 5, 6 ])
        self.assertEquals(result[0].proposal, ctx.p1) # won 1, has lowest id
        self.assertEquals(result[1].proposal, ctx.p6) # won 1, higher id
        self.assertEquals(result[2].proposal, ctx.p3) # tied 1, lower id
        self.assertEquals(result[3].proposal, ctx.p4) # tied 1, higher id
        self.assertEquals(result[4].proposal, ctx.p2) # lost 1, lower id
        self.assertEquals(result[5].proposal, ctx.p5) # lost 1, higher id

class PlayerTestCases(JudgeTestCases):
    def setUp(self):
        super(PlayerTestCases, self).setUp()
        self.calculator = StandingsCalculator()
        self.player = Player(hashie(id=666), 0)

    def test_compute_victory(self):
        self.player.add_result('victory')
        self.player.add_result('victory')
        self.assertEquals(self.player.points, 6)
        self.assertEquals(self.player.victories, 2)

    def test_compute_ties(self):
        self.player.add_result('tie')
        self.assertEquals(self.player.points, 1)
        self.assertEquals(self.player.ties, 1)

    def test_compute_defeats(self):
        self.player.add_result('defeat')
        self.assertEquals(self.player.points, 0)
        self.assertEquals(self.player.defeats, 1)

    def test_sort_by_id_by_default(self):
        p1 = Player(hashie(id=123), 0)
        p2 = Player(hashie(id=456), 0)
        self.assertGreater(p1, p2)

    def test_sort_by_points(self):
        p1 = Player(hashie(id=1), 3)
        p2 = Player(hashie(id=2), 6)
        self.assertGreater(p2, p1)

    def test_sort_by_victories_if_points_are_tied(self):
        p1 = Player(hashie(id=123), 0, victories=0, ties=3)
        p2 = Player(hashie(id=456), 0, victories=1, ties=0)
        self.assertGreater(p2, p1)
