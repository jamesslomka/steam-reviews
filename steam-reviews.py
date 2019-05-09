#!/usr/bin/python3

import requests
import unicodecsv as csv
from bs4 import BeautifulSoup
with open("steam_data.csv", 'wb') as f:
    writer = csv.writer(f, dialect='excel')
    writer.writerow(["UserID", "SteamID", "Game Title", "AppID", "Recommended?", "Review", "Date Posted", "Hours Played"])

# getting userIDs from csv file
with open("steamid.csv",'rb') as file:
    reader = csv.reader(file)
    userID = 0
    for steamID in reader:
        print("Checking user " + str(userID) + " with steamID:  " + str(steamID[0]) + "\n")
        userID = userID + 1
        # if-statement (James)
        if userID <= 10000:
            print(userID)
            x = 1
            # hardcoded assuming no more than 999 reviews
            for x in range(1,100):
                url = "https://steamcommunity.com/profiles/" + steamID[0] + "/recommended/?p=" + str(x)
                x = x + 1
                user = userID - 1
                response = requests.get(url)
                soup = BeautifulSoup(response.content, "html.parser")
                game_url = []
                game_title = []
                appid = []
                recommended = []
                reviews = []
                dateL = []
                hours = []
                checkReviews = soup.find_all('div', {'class': 'rightcol'})
                title = soup.find_all('div', {'class':'leftcol'})
                recommend = soup.find_all('div', {'class':'title'})
                date = soup.find_all('div', {'class': 'posted'})
                time = soup.find_all('div', {'class': 'hours'})
                getAppid = soup.find_all('div', {'class':'title'})

                if not checkReviews:
                    print("***** No Reviews *****\n")
                    break

                else:
                    print("----- Reviews Found ------\n")
                    for counter in range(len(checkReviews)):
                        try:
                            # get game title
                            game_url.append(title[counter].find('a')['href'])
                            response = requests.get(game_url[counter])
                            soup = BeautifulSoup(response.content,"html.parser")
                            game = soup.title.string.replace("™","")
                            game = game.replace("®","")
                            game = game.replace("Steam Community :: ", "")
                            game_title.append(game)
                            print(game_title[counter] + "\n")
                            # get appid
                            get_appid = game_url[counter].replace("http://steamcommunity.com/app/","")
                            appid.append(get_appid)
                            print(get_appid)
                            # getting reviews
                            reviews.append(checkReviews[counter].find('div',{'class': 'content'}).get_text())
                            print(reviews[counter].strip() + "\n")
                            # getting hours played
                            hours_played = time[counter].get_text().replace(" hrs on record", "")
                            hours.append(hours_played.strip())
                            print("hours played: " + hours[counter])
                            # get recommended
                            recommended.append(recommend[counter].get_text())
                            print(recommended[counter].strip())
                            # getting date
                            date_posted = date[counter].get_text()
                            dateL.append(date_posted.strip())
                            print(dateL[counter])
                        except TypeError:
                            pass
                        except IndexError:
                            pass
                        except requests.exceptions.RequestException:
                            pass
                        except:
                            pass
                # write to csv
                with open("steam_data.csv",'ab') as f:
                    writer = csv.writer(f, encoding='utf-8')
                    for i in range(len(game_title)):
                        try:
                            writer.writerow([user, steamID[0], game_title[i], appid[i], recommended[i], reviews[i], dateL[i], hours[i]])
                        except UnicodeEncodeError:
                            try:
                                writer.writerow([user, steamID[0], game_title[i], appid[i], recommended[i], "could not encode text", dateL[i], hours[i]])
                            except UnicodeEncodeError:
                                pass
