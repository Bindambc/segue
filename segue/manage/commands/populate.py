 # -*- coding: latin-1 -*-
from segue.core import db
from tests.support.factories import *
from segue.models import Account, Proposal, ProposalInvite, Track

def populate(clean=False):
    if clean:
        ProposalInvite.query.delete()
        Proposal.query.delete()
        Account.query.delete()
        populate_reference_data(True)

    accounts = [
        ValidAccountFactory.build(password='1234'),
        ValidAccountFactory.build(password='1234'),
        ValidAccountFactory.build(password='1234'),
    ]
    proposals = [
        ValidProposalFactory.build(owner=accounts[0]),
        ValidProposalFactory.build(owner=accounts[0]),
        ValidProposalFactory.build(owner=accounts[1]),
        ValidProposalFactory.build(owner=accounts[1]),
    ]
    proposal_invites = [
        ValidInviteFactory.build(proposal=proposals[0]),
        ValidInviteFactory.build(proposal=proposals[0]),
        ValidInviteFactory.build(proposal=proposals[0]),
    ]

    db.session.add_all(accounts)
    db.session.add_all(proposals)
    db.session.add_all(proposal_invites)
    db.session.commit()

def populate_reference_data(clean=False):
    if clean:
        Track.query.delete()

    tracks = [
        #Zona Administra��o
        ValidTrackFactory(name_pt=u'Administra��o - Administra��o de Sistemas',
                          name_en=u'Administration - Systems Administration'),
        
        ValidTrackFactory(name_pt=u'Administra��o - Bancos de Dados',
                          name_en=u'Administration - Databases'),
        
        ValidTrackFactory(name_pt=u'Administra��o - Sistemas operacionais',
                          name_en=u'Administration - Operating Systems'),
        
        ValidTrackFactory(name_pt=u'Administra��o - Seguran�a',
                          name_en=u'Administration - Security'),
        
        #Zona Desenvolvimento
        ValidTrackFactory(name_pt=u'Desenvolvimento - Ferramentas, Metodologias e Padr�es',
                          name_en=u'Development - Tools, Methodologies and Standards'),
        
        ValidTrackFactory(name_pt=u'Desenvolvimento - Ger�ncia de Conte�do / CMS',
                          name_en=u'Development - Content Management / CMS'),
        
        ValidTrackFactory(name_pt=u'Desenvolvimento - Linguagens de programa��o',
                          name_en=u'Development - Programming Languages'),
        
        #Zona Desktop
        ValidTrackFactory(name_pt=u'Desktop - Aplica��es Desktop',
                          name_en=u'Desktop - Desktop Applications'),
        
        ValidTrackFactory(name_pt=u'Desktop - Multim�dia',
                          name_en=u'Desktop - Multimedia'),
        
        ValidTrackFactory(name_pt=u'Desktop - Jogos',
                          name_en=u'Desktop - Games'),
        
        ValidTrackFactory(name_pt=u'Desktop - Distribui��es',
                          name_en=u'Desktop - Distros'),
        
        #Zona Ecossistema
        ValidTrackFactory(name_pt=u'Ecossistema - Cultura, Filosofia, e Pol�tica',
                          name_en=u'Ecosystem - Culture, Philosophy, and Politics'),
        
        ValidTrackFactory(name_pt=u'Ecossistema - Neg�cios, Migra��es e Casos',
                          name_en=u'Ecosystem - Business, Migrations and Cases'),
        
        #Zona Educa��o
        ValidTrackFactory(name_pt=u'Educa��o - Inclus�o Digital',
                          name_en=u'Education - Digital Inclusion'),
        
        ValidTrackFactory(name_pt=u'Educa��o - Educa��o',
                          name_en=u'Education - Education'),
        
        #Zona Encontros Comunit�rios
        ValidTrackFactory(name_pt=u'Encontros Comunit�rios - Principal',
                          name_en=u'Community Meetings - Main'),
        
        ValidTrackFactory(name_pt=u'Encontros Comunit�rios - ASL',
                          name_en=u'Community Meetings - ASL'),
        
        ValidTrackFactory(name_pt=u'Encontros Comunit�rios - WSL',
                          name_en=u'Community Meetings - WSL'),
        
        #Zona T�picos Emergentes
        ValidTrackFactory(name_pt=u'T�picos Emergentes - Hardware Aberto',
                          name_en=u'Trending Topics - Open Hardware'),
        
        ValidTrackFactory(name_pt=u'T�picos Emergentes - Dados Abertos',
                          name_en=u'Trending Topics - Open Data'),
        
        ValidTrackFactory(name_pt=u'T�picos Emergentes - Acesso Aberto',
                          name_en=u'Trending Topics - Open Access'),
        
        ValidTrackFactory(name_pt=u'T�picos Emergentes - Governan�a da Internet',
                          name_en=u'Trending Topics - Internet Governance'),
        
        ValidTrackFactory(name_pt=u'T�picos Emergentes - Privacidade e Vigil�ncia',
                          name_en=u'Trending Topics - Privacy and Surveillance'),
        
        ValidTrackFactory(name_pt=u'T�picos Emergentes - Energia Livre',
                          name_en=u'Trending Topics - Free Energy'),
    ]
    db.session.add_all(tracks)
    db.session.commit()
