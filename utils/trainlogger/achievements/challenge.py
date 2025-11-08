import os


def checkChallengeAchievements(user):
    """made for zhang's challenge thing"""
    filepath = f"utils/trainlogger/userdata/{user}.csv"
    if not os.path.exists(filepath):
        filepath = None
        return []

    new_achievements = []
