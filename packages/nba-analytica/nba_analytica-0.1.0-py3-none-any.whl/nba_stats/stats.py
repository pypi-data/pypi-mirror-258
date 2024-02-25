import requests

def get_player_stats(player_name: str, per_mode='PerGame'):
    """
    Fetch NBA player statistics from the stats.nba.com API.

    Parameters:
    - player_name (str): The name of the player for whom to fetch stats.
    - per_mode (str): The mode of the statistics. Options are:
        - 'PerGame' for stats per game.
        - 'PerPossession' for stats per possession.
        - 'Per100Possessions' for stats per 100 possessions.
    
    Returns:
    - dict: A dictionary containing the player's statistics if found.
    - str: An error message if the player is not found or if the API request fails.

    Raises:
    - ValueError: If the provided per_mode is not one of the allowed options.

    Example usage:
     >>> get_player_stats('LeBron James', 'PerGame')
    { 'PLAYER_NAME': 'LeBron James', 'PTS': 25.3, ... }
    """

    allowed_per_modes = ['PerGame', 'PerPossession', 'Per100Possessions']
    if per_mode not in allowed_per_modes:
        raise ValueError(f"Invalid per_mode. Allowed values are: {allowed_per_modes}")

    url = f"https://stats.nba.com/stats/leaguedashplayerstats?Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&ISTRound=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode={per_mode}&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2023-24&SeasonSegment=&SeasonType=Regular%20Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&tCollege=&Weight="

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Host": "stats.nba.com",
        "Referer": "https://www.nba.com/",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        player_stats_headers = data["resultSets"][0]["headers"]
        player_stats_data = data["resultSets"][0]["rowSet"]

        player_stats_by_name = {}
        for player in player_stats_data:
            if player[player_stats_headers.index("PLAYER_NAME")] == player_name:
                player_stats_by_name = {player_stats_headers[i]: player[i] for i in range(len(player_stats_headers))}
                break

        return player_stats_by_name if player_stats_by_name else f"No data for player named {player_name}"
    else:
        return f"Request failed with status code: {response.status_code}"