from django.core.management.base import BaseCommand
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient(host='localhost', port=27017)
        db = client['octofit_db']

        # Collections
        users = db['users']
        teams = db['teams']
        activities = db['activities']
        leaderboard = db['leaderboard']
        workouts = db['workouts']

        # Clear collections
        users.delete_many({})
        teams.delete_many({})
        activities.delete_many({})
        leaderboard.delete_many({})
        workouts.delete_many({})

        # Create unique index on email
        users.create_index([('email', 1)], unique=True)

        # Sample teams
        marvel_team = {'name': 'Marvel', 'members': ['Iron Man', 'Captain America', 'Thor', 'Black Widow']}
        dc_team = {'name': 'DC', 'members': ['Superman', 'Batman', 'Wonder Woman', 'Flash']}
        teams.insert_many([marvel_team, dc_team])

        # Sample users
        user_docs = [
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': 'Marvel'},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team': 'Marvel'},
            {'name': 'Thor', 'email': 'thor@marvel.com', 'team': 'Marvel'},
            {'name': 'Black Widow', 'email': 'widow@marvel.com', 'team': 'Marvel'},
            {'name': 'Superman', 'email': 'superman@dc.com', 'team': 'DC'},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': 'DC'},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': 'DC'},
            {'name': 'Flash', 'email': 'flash@dc.com', 'team': 'DC'},
        ]
        users.insert_many(user_docs)

        # Sample activities
        activities.insert_many([
            {'user': 'Iron Man', 'activity': 'Running', 'duration': 30},
            {'user': 'Batman', 'activity': 'Cycling', 'duration': 45},
            {'user': 'Wonder Woman', 'activity': 'Swimming', 'duration': 60},
            {'user': 'Flash', 'activity': 'Sprinting', 'duration': 15},
        ])

        # Sample leaderboard
        leaderboard.insert_many([
            {'team': 'Marvel', 'points': 120},
            {'team': 'DC', 'points': 110},
        ])

        # Sample workouts
        workouts.insert_many([
            {'user': 'Thor', 'workout': 'Weightlifting', 'reps': 100},
            {'user': 'Superman', 'workout': 'Pushups', 'reps': 200},
        ])

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
