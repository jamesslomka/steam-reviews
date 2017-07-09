import requests
import csv
from bs4 import BeautifulSoup

# Getting userID's from csv file
with open("steamid.csv","r") as file:
	reader = csv.reader(file)
	userID = 1

	for steamID in reader:
		print("Checking user " + str(userID) + " with steamID:  " + str(steamID[0]) + "\n")
		userID = userID + 1
		url = "https://steamcommunity.com/profiles/" + steamID[0] + "/recommended/?p=1"
		response = requests.get(url)
		soup = BeautifulSoup(response.content,"html.parser")

		reviews = []
		game_url = []
		game_title = []
		dateL = []
		checkReviews = soup.find_all('div', {'class': 'rightcol'})
		title = soup.find_all('div', {'class':'leftcol'})
		date = soup.find_all('div', {'class': 'posted'})
		time = soup.find_all('div', {'class': 'hours'})

		if not checkReviews:
			print("***** No reviews ******* \n")
		else:
			print("----- Reviews Found ------\n")
			for counter in range(len(checkReviews)):
				# getting reviews
				reviews.append(checkReviews[counter].find('div',{'class': 'content'}).get_text())
				print(reviews[counter].strip() + "\n")
				# get game title
				game_url.append(title[counter].find('a')['href'])
				response = requests.get(game_url[counter])
				soup = BeautifulSoup(response.content,"html.parser")
				game_title.append(soup.title.string)
				print(game_title[counter] + "\n")
				# getting date
				dateL.append(date[counter].get_text())
				print(dateL[counter].strip())
				# getting hours played
					#  --> add hours <--
