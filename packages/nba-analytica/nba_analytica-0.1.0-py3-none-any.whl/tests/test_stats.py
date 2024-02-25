import unittest
from unittest.mock import patch
from nba_stats import get_player_stats

class TestNBAStats(unittest.TestCase):

    @patch('nba_stats.stats.requests.get')
    def test_get_player_stats_success(self, mock_get):
        # Mock the API response to simulate a successful API call
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "resultSets": [{
                "headers": ["PLAYER_NAME", "PTS"],
                "rowSet": [
                    ["LeBron James", 25]
                ]
            }]
        }

        result = get_player_stats("LeBron James")
        self.assertIsNotNone(result)
        self.assertEqual(result["PTS"], 25)

    @patch('nba_stats.stats.requests.get')
    def test_get_player_stats_failure(self, mock_get):
        # Simulate a player not found situation
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "resultSets": [{
                "headers": ["PLAYER_NAME", "PTS"],
                "rowSet": []
            }]
        }

        result = get_player_stats("Unknown Player")
        self.assertIn("No data for player named", result)

if __name__ == '__main__':
    unittest.main()
