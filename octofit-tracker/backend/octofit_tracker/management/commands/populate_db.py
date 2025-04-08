from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import timedelta
from django.conf import settings
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activity, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Clear existing data using raw MongoDB commands to avoid Django ORM issues
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        db.users.delete_many({})
        db.teams.delete_many({})
        db.activity.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Ensure no duplicate users exist by dropping the entire users collection
        db.users.drop()

        # Recreate users collection to start fresh
        db.create_collection('users')

        # Use raw MongoDB commands to delete users to avoid Django ORM issues
        db.users.delete_many({"email": {"$in": [
            'thundergod@mhigh.edu',
            'metalgeek@mhigh.edu',
            'zerocool@mhigh.edu',
            'crashoverride@mhigh.edu',
            'sleeptoken@mhigh.edu'
        ]}})

        # Ensure users are created and fetched correctly without duplication
        users = {
            'thundergod': User.objects.create(email='thundergod@mhigh.edu', name='Thor', age=30),
            'metalgeek': User.objects.create(email='metalgeek@mhigh.edu', name='Tony Stark', age=35),
            'zerocool': User.objects.create(email='zerocool@mhigh.edu', name='Steve Rogers', age=32),
            'crashoverride': User.objects.create(email='crashoverride@mhigh.edu', name='Natasha Romanoff', age=28),
            'sleeptoken': User.objects.create(email='sleeptoken@mhigh.edu', name='Bruce Banner', age=40),
        }

        # Create teams
        team1 = Team(name='Blue Team')
        team2 = Team(name='Gold Team')
        team1.save()
        team2.save()

        # Create activities using the user dictionary
        activities = [
            Activity(user=users['thundergod'], type='Cycling', duration=60, date='2025-04-08'),
            Activity(user=users['metalgeek'], type='Crossfit', duration=120, date='2025-04-07'),
            Activity(user=users['zerocool'], type='Running', duration=90, date='2025-04-06'),
            Activity(user=users['crashoverride'], type='Strength', duration=30, date='2025-04-05'),
            Activity(user=users['sleeptoken'], type='Swimming', duration=75, date='2025-04-04'),
        ]
        for activity in activities:
            activity.save()

        # Create leaderboard entries
        leaderboard_entries = [
            Leaderboard(user=users['thundergod'], score=100),
            Leaderboard(user=users['metalgeek'], score=90),
            Leaderboard(user=users['zerocool'], score=95),
            Leaderboard(user=users['crashoverride'], score=85),
            Leaderboard(user=users['sleeptoken'], score=80),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)

        # Create workouts
        workouts = [
            Workout(name='Cycling Training', description='Training for a road cycling event', duration=60),
            Workout(name='Crossfit', description='Training for a crossfit competition', duration=120),
            Workout(name='Running Training', description='Training for a marathon', duration=90),
            Workout(name='Strength Training', description='Training for strength', duration=30),
            Workout(name='Swimming Training', description='Training for a swimming competition', duration=75),
        ]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))