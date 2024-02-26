<h1 align="center">💫 RiotWrapper 💫</h1>
<p align="center">
  <em>Riot API made easy</em>
</p>

🚀 **Features**

RiotWrapper is a Python library with a number of classes designed to facilitate interactions with the Riot Games API. Here's what it can do:

*RiotWrapper*: Your primary interface with the API. Initializes essential details like the API key, region, and debug mode.

*RequestHandler*: In charge of crafting requests to the Riot Games API, and leverages UrlBuilder and ResponseChecker for URL building and response validation.

*UrlBuilder*: Constructs request URLs based on the specified range.

*ResponseChecker*: Checks the status of responses, raising an exception if the response is not ​200.

*MatchApi* and *SummonerApi*: Enable querying of match and player informations.<br><br>

🛠️ **Usage**

For the moment you can use __'main.py'__ to start off but this will disappear at some point.

Or here's a quick start guide to get you up and running:


    from RiotWrapper import RiotWrapper

    # Initialize RiotWrapper with your API key and region
    euw1_rw = RiotWrapper(api_key="your_api_key", region="euw1")

    # Fetch match details by its ID
    match_info = euw1_rw.match.by_match_id(match_id="your_match_id")

    # Fetch player details by its name
    summoner_info = euw1_rw.summoner.by_name(summoner_name="your_summoner_name")

<br>

⌛ **Future improvements**

*Implementing all other endpoints for LoL:*
  - Champion-v3
  - Account-v1
  - Champion Mastery-v4

*Refining actual endpoints :*
  - Summoner-v4
  - Match-v5

*Random stuff :*
  - Add Handling HTTP exceptions 
  - Add pip support
