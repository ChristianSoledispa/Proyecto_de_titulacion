import instaloader
import pandas as pd
 
# Creating an instance of the Instaloader class
bot = instaloader.Instaloader()
 
# Loading a profile from an Instagram handle
cuenta=input("Ingresa el nombre de usuario a realizar scraping:")
profile = instaloader.Profile.from_username(bot.context, cuenta)

# L = instaloader.Instaloader()

# id = 'user'
# pw = 'password.'

# L.load_session(id, pw)
# L.login(id, pw)
print("Username: ", profile.username)
print("User ID: ", profile.userid)
print("Number of Posts: ", profile.mediacount)
print("Followers Count: ", profile.followers)
print("Following Count: ", profile.followees)
print("Bio: ", profile.biography)
print("External URL: ", profile.external_url)

