#!/usr/bin/env python
# coding: utf-8

# ## FINDING THE BEST APP TYPE: ##
# our project consists in analyzing andriod and ios stores data with the purpose of finding out whats the best category to make a profitable free in_app ad app. which category would attract more users?

# In[6]:


#first lets open the files #

opened_ios = open('./Downloads/AppleStore.csv', encoding = 'utf8')
opened_android = open('./Downloads/googleplaystore.csv', encoding = 'utf8')

#then we need to import the csv reader to read it and store in the lists

from csv import reader
readed_ios = reader(opened_ios)
readed_android = reader(opened_android)

#once they are readed, we can store it inside lists

ios_data = list(readed_ios)
android_data = list(readed_android)


# lets create a function that helps us explore the data

# In[56]:


#this function will help in printing rows repeatedly in a readable way
def explore_data(dataset, start, end, rows_and_columns= False):
    dataset_slice = dataset[start:end]
    for row in dataset_slice:
        print(row)
        print('\n')  # adds a new empty line after each row to help readability #
        
    if rows_and_columns == True:
        print('Number of rows', len(dataset))
        print('Number of columns', len(dataset[0]))
        


# lets make some short analysis of the dimensions and columns of both datasets. the meaning of the columns of google play store are not described by the dataset owner, but from the apple store dataset.

# In[58]:


print('Google Play Store apps data columns and dimensions \n')
explore_data(android_data, 0, 1, True)
print('\n', '-'*60, '\n')

print('Apple Store apps columns and dimensions \n')
explore_data(ios_data, 0, 1, True)


# looking at the columns of our dataset we can identify some important information that we will use to answer our main question like:
# Google Play Store = 'App', 'category', 'Rating', 'Installs', 'Type', 'Price', 'Genres'
# App Store = 'id', 'price', 'rating_count_tot', 'user_rating', 'cont_rating', 'prime_genre'
# 
# now we will store the columns names in a different list so that we can use it for future reference

# In[60]:


# android column names
columns_android = android_data[0]

# ios column names

columns_ios = ios_data[0]


print('Ándroid columns\n', columns_android)
print('\niOS columns\n', columns_ios)


# ## 2. CLEANING DATA ##
# 
# before any data analysis is carried out, it is extremely important that data assessment is carried out. data assessment include data cleaning, removing duplicates, checking for accuracy of data and so on.
# 
# ## 2.1 Checking for wrong data ##
# 
# checking the discussion forum of our dataset we can see theres an erorr in row 10472(actually 10473). we print it to be sure, then we'll delete it.

# In[10]:


android_data[10473] # this particular row does not have category in it, so have to delete it because it is not in line with other dataset


# In[11]:


del android_data[10473] #deleting row 10473 from the dataset

#to check if its gone
explore_data(android_data, 0, 1, True)


# checking for other wrong data

# In[12]:


#looking at instagram entries

for app in android_data:
    name = app[0]
    if name == 'Instagram':
        print(app)


# fully aware that there is duplicate, we will create a function that gives us the number of duplicates and store the name of duplicates, so that we can remove the duplicates

# In[13]:


#first we will store the duplicates values into list
duplicated = []
unique = []

for app in android_data:
    name = app[0]
    if name in unique:
        duplicated.append(name)
    else:
        unique.append(name)
        
#then we can see how many entries each list have
print(len(duplicated))
print(len(unique))


# with that in mind, we wont remove the duplicates randomly. looking at the 'instagram' entries we printed, we can see the 4th column has the number of reviews, thinking about it logically we can see that the biggest number reflects the newer entry. this is the entry we are going to keep.

# In[14]:


#creating a dictionary to store name and maximum
reviews_max = {}

#looping through the data to populate the dictionary
for app in android_data[1:]:  #excluding the header column
    name = app[0]
    n_reviews = float(app[3])
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
    elif name not in reviews_max:
        reviews_max[name] = n_reviews
        
#seeing if everything went fine
print('size of reviews_max dictionary', len(reviews_max))
    


# now that we have created this dictionary with entries(name of the app and amount of reviews), we can go back to our main data set and start to remove the ones that are not there.
# 
# the loop consists in checking two things:
# 1) if the number of reviews from our main dataset is equal to the one stored in our dictionary with the max review number, showing that this entry is the newest.
# 2)if the entry has already been added(it checks if it already exists in the already_added list).
# 
# once the entry has the same number of review and hasn't been added, it will be stored in our new list created to recieve the cleaned data android_clean.
# 
# finally we print the length of the list to see if everything went fine (it has to be the same length as th reviews_max that we did above

# In[15]:


# Creating a list to store our cleaned data
android_clean = []

# Creating a help list to store the app names
already_added = []

# looping through the data to clean it
for app in android_data[1:]:
    name = app[0]
    n_reviews = float(app[3])
    if n_reviews == reviews_max[name] and name not in already_added:
        android_clean.append(app)
        already_added.append(name) 
print('size of android_clean list', len(android_clean))


# ## LOOKING FOR DUPLICATES IN APPLE STORE ##
# 
# using a similiar approach we are going to insert the unique ids in the list unique and the repeated ones in the duplicated. then we'll see the length of them

# In[16]:


# creating the list

unique = []
duplicated = []

# adding values to the empty list above:
for app in ios_data:
    app_id = app[0]
    if app_id in unique:
        duplicated.append(app_id)
    else:
        unique.append(app_id)
        
#checking to see how it looks like
print('unique values: {} \nduplicated values: {}'.format(len(unique), len(duplicated)))


# As we can see there are no duplicated values in the dataset. but other issues comes, when we think that our company wants to develop an app to the english speaking audience, we need to remove the apps that are not in english. and in both datasets we see this type of entry.
# 
# ## REMOVING THE NON ENGLISH APPS ##
# 
# 

# In[17]:


# printing non english apps in the ios dataase
print('Apple store non-english apps: \n \n{} \n{}\n'.format(ios_data[814][1], ios_data[6732][1]))

#printing non-english app in the android database
print('\nGoogle Play Store non-english apps: \n \n{} \n{}'.format(android_clean[4412][0],android_clean[7940][0]))


# in order to remove non english apps that have characters that are not contained in English language. we can know that by the index of every letter(this is found with the ord() built_in function), the characters from the english alphabet are in the range of 0 to 127 (according to the ASCII)
# 
# with that in mind, we are going to create a function that sees if the app name has non-english characters GoTM
# 

# In[25]:


# loops over the chars and see if they have any non-english characters
def english_char(a_string):
    for char in a_string:
        if ord(char) > 127:
            return False
    return True

# lets check some values
print('Instagram is engish-language app. \t\t\t\t', english_char('Instagram'))
print('爱奇艺PPS -《欢乐颂2》电视剧热播 is an english app.\t\t', english_char('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print('Docs To Go™ free office Suite is an english app.\t\t', english_char('Docs To Go™ free office Suite'))
print('Instachat 😜 is an english-language app.\t\t\t', english_char('Instachat 😜'))


# the reason that our function returns 'Instachat 😜' and 'Docs To Go™ free office Suite' as non english language apps is because of characters like TM fall outside the ASCII range and have numbers over 127.
# 
# we cannot exclude this values from our dataset, since it is really useful. To fix it in some way, we will allow our strings to have maximum 3 special characters. abaelow we will rewrite our function to do that.

# In[26]:


# loops over the chars and see if they have more than 3 non-english characters
def english_char(a_string):
    special_char = 0
    for char in a_string:
        if ord(char) > 127:
            special_char += 1
    if special_char >= 3:
        return False
    else:
        return True
    
#let's check some values
print('Instagram is engish-language app. \t\t\t\t', english_char('Instagram'))
print('爱奇艺PPS -《欢乐颂2》电视剧热播 is an english app.\t\t', english_char('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print('Docs To Go™ free office Suite is an english app.\t\t', english_char('Docs To Go™ free office Suite'))
print('Instachat 😜 is an english-language app.\t\t\t', english_char('Instachat 😜'))


# Now we'll use our new function to filter the apps that are in english language and make our dataset cleaner.

# In[28]:


#cleaning the android data
play_store_data = []
for app in android_clean[1:]:
    name = app[0]
    if name not in android_data:
        if english_char(name) == True:
            play_store_data.append(app)
            
a = len(android_clean)
b = len(play_store_data)

print('the new clean dataset has {} entries and the older had {}, {} entries were removed'.format(b, a, a-b))


# In[30]:


# cleaning the ios_data
app_store_data = []

for app in ios_data[1:]:
    app_id = app[0]
    if app_id not in app_store_data:
        if english_char(app_id) == True:
            app_store_data.append(app)
            
a = len(ios_data)
b = len(app_store_data)
print('the new clean dataset has {} entries and the older had {}, {} entries were removed'.format(b, a, a-b))


# Now that we made it we have just another thing to do. Since our company wants to create a free app with ads in it, we need to separate the free apps from the non-free apps. This is the last step of our data cleaning process

# ## 2.5 Separating the free from the non-free apps ##
# 
# First we will check in which column the prices are in both datasets

# In[32]:


print(columns_android)
print('\n')
print(columns_ios)


# From the output above, we can see we need the 8th column of android data and the 5th of the ios data. Knowing this, we will start the operation

# In[39]:


#creating list to store free apps
free_android_apps = []
free_ios_apps = []

for app in play_store_data:
    price = float(app[7].replace('$', ''))
    if price == 0.00:
        free_android_apps.append(app)
        
for app in app_store_data:
    price = float(app[4].replace('$', ''))
    if price == 0.00:
        free_ios_apps.append(app)
        
print('number of free android apps is', len(free_android_apps))
print('number of all android apps is', len (play_store_data))
print('\nnumber of free ios apps is', len(free_ios_apps))
print('number of all ios apps is', len(app_store_data))


# ## 3 Analyzing data ##
# 
# Thinking about the primary objective(launch an app in App Store and Play Store), we need to evaluate both platforms. To minimize the risk the validation strategy for an app idea is comprised of three steps(as said in our DataQuesr course):
# 
#      1. Build a minimal Android version of the app, and add it to GOogle play
#      2. If the app has a good response from users, we develop it further
#      3. If the app is profitable after six months, we build an IOS version of the app and add it to the App store
#      
# To do so, we are going to use the genres column (index 9) and category column(index 1) in Google play store dataset and the prime_genre column (index 11) in our App Store dataset.
# 
# To analyze it this way, we are going to make two functions: one to make the frequency tables with percentages and another to put the percentages in descending order.

# In[42]:


# making a function that creates a frequency table that shows percentages
def freq_table(dataset, index):
    frequency_table = {}
    total = len(dataset)
    for row in dataset:
        entry = row[index]
        if entry in frequency_table:
            frequency_table[entry] += 1
        else:
            frequency_table[entry] = 1
            
    for key in frequency_table:
        frequency_table[key] /= total/100
        frequency_table[key] = round(frequency_table[key], 4)
        
    return frequency_table

#check to see whether the first entries of dictionary will print
print(list((freq_table(free_android_apps, 1)).items())[:10])


# Above we have created the dictionary and it worked. to slice it we have printed a slice of a list made with its items(dictionaries cannot be sliced), we didnt change the dictionary, we just printed it in a different way. lets do the same thing with the App store data.

# In[43]:


# making a function that displays the percentages in a descending order
# this function was already made by Dataquest, they claimed that this is easier with other resources

def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


# In[45]:


# display table for free_android_apps genre

display_table(free_android_apps, 9)


# In[47]:


# display free_android_apps categories

display_table(free_android_apps, 1)


# In[49]:


# display table for free_ios_apps prime_genres

display_table(free_ios_apps, 11)


# relevant questions to answer about our data:
# 
# 1) What is the most common genre? What is the runner-up?
# 2) What patterns can we see?
# 3) What is the general impression- are most apps designed for practical purposes or more for entertainment?
# 4) Could we recommend and app profile based on the information we have so far? Does a bi amount of apps in that genre imply a large number of users?

# With that in mind we can see that App Store has a big amount of entertainment apps, on the other hand Play Store is more balanced, having productivity, education and business in the top 5. But this data isnt enough to set a strategy. we need to know how many people have downloaded this apps.
# The Play Store dataset has a column called intalls(index5) that gives us already this information. App Store dataset does not have this information, the solution is to look at the total number of user rating in the rating_count_tot(index 5), since we don't have a better option. Next we are going to calculate the average number of user ratings per app genre in App Store

# In[50]:


# making a frequency table for prime_genre
prime_genre_freq = freq_table(free_ios_apps, 11)

for genre in prime_genre_freq:
    total = 0
    len_genre = 0
    for app in free_ios_apps:
        genre_app = app[11]
        if genre_app == genre:
            n_ratings = float(app[5])
            total += n_ratings
            len_genre += 1
    avg_ratings = round(total/len_genre, 4)
    genre_ratings = [genre, avg_ratings]
    print(genre, genre_ratings)


#    ## looking at the data we have analyzed so far, we can see that in App Store good ideas of apps would be in Social Networking, reference, weather or music field, since the four of them have more than 40 thousand ratings(indicating a lot of downloads) and they are not saturated: Music apps are 1.65% of our dataset, weather 0.76%, Social Networking 3.53% and reference 0.49% ##

# Now we need to evaluate the amount of installs of the apps from the Play Store. They do not have an exact number for each apps, so we are goin to work with have. Once we take this values, we will treat them and print so we can analyze it.

# In[52]:


# making a frequency table for category (playstore)
category_freq = freq_table(free_android_apps, 1)

for category in category_freq:
    total = 0
    len_category = 0
    for app in free_android_apps:
        category_app = app[1]
        if category_app == category:
            n_ratings = float((app[5].replace('+', '')).replace(',',''))
            total += n_ratings
            len_category += 1
    avg_ratings = round(total/len_category, 4)
    category_ratings = [category, avg_ratings]
    print(category, avg_ratings)


# In[53]:


# making a frequency table for category/genre column(Play Store)
genre_freq = freq_table(free_android_apps, 9)

for genre in genre_freq:
    total = 0
    len_genre = 0
    for app in free_android_apps:
        genre_app = app[9]
        if genre_app == genre:
            n_ratings = float((app[5].replace('+', '')).replace(',',''))
            total += n_ratings
            len_genre += 1
    avg_ratings = round(total/len_genre, 4)
    genre_ratings = [genre, avg_ratings]
    print(genre, avg_ratings)


# ## looking at the data we have printed, we can see that the most installed apps that are not a big part of the total apps are:
# 
# 1)Video players more than 24million downloads and 1.79%
# 2) Entertainment with more than 11million downloads and 0.96% of total apps
# 3) Books and references with more than 8million downloads and 2.13% of total apps
# 4) Weather with more than 5million downloads and 0.79% of total apps
# 5) Music with more than 9million downloads and 0.30%(approximately) of total apps

# ## keeping in mind that we want an app for both platforms(play store and app store), books, references, music app are good choices, since they are downloaded alot and have a small share in the total number of apps in both markets. To refine our decision, we are going to take a look in these specific genres to see if there's something interesting there

# # Books, references and Music apps analysis

# In[54]:


# making a list with all book and reference android apps
books_android = []
for app in free_android_apps:
    category = app[1]
    if category == 'BOOKS_AND_REFERENCE':
        books_android.append(app)
        
#making a list with all music android apps
music_android = []
for app in free_android_apps:
    genre = app[9]
    if 'Music' in genre:
        music_android.append(app)
        
#making list with all book and reference ios apps

books_ios =[]
for app in free_ios_apps:
    category = app[11]
    if category == 'Reference':
        books_ios.append(app)
    elif category == 'Book':
        books_ios.append(app)
        
#making a list with all music ios apps
music_ios = []
for app in free_ios_apps:
    category = app[11]
    if category == 'Music':
        music_ios.append(app)

print('lenth of books_android (and references)', len(books_android))
print('length of music_android:', len(music_android))
print('\n')
print('length of books_ios (and references):', len(books_ios))
print('length of music_ios', len(music_ios))


# In[ ]:




