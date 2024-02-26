from .Endpoints import *

class RiotWrapper:
    def __init__(self, api_key, region, use_cache=True):
        # TODO: add api class
        # self.api = Api(region, api_key)
        # self.summoner = SummonerApi()

        self.summoner = summoner_v4.SummonerApi(region, api_key, use_cache)
        self.match = match_v5.MatchApi(region, api_key, use_cache)
        self.champion = champion_v3.ChampionApi(region, api_key, use_cache)
        self.mastery = championMastery_v4.ChampionMasteryApi(region, api_key, use_cache)
        self.league = league_v4.LeagueApi(region, api_key, use_cache)
        self.spectator = spectator_v4.SpectatorApi(region, api_key, use_cache)
        self.league_exp = leagueExp_v4.LeagueExpApi(region, api_key, use_cache)
        self.lol_status = lolStatus_v4.LolStatusApi(region, api_key, use_cache)
        self.account = account_v1.AccountApi(region, api_key, use_cache)
        
        


    
    
    

    
    # get winrate ?
    # general functions to get stats ?
    # get games played with count ?
    # stats by champion ?
    # stats by role ?
    # average stats ?
    # random games picked ?
    # change champion id to champion name ?