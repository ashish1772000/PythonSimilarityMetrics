# read the external movie file and load the information in the structured way to the data dictionary 
def load_moviedetails():     
    users = {}                                                      # declare user preference dictionary
    movie_genres_and_watchers = {}                                  # declare movie genres and watchers dictionary    
    try:       
        with open('u.data', 'r', encoding='ISO-8859-1') as usrfile: # collect userids for the movies            
            for lne in usrfile:                                     # read each line of the file 
                (usrid, movid, rat, tstamp) = lne.split('\t')[0:4]  # set variables to store the individual information                
                users.setdefault(movid, []).append(usrid)           # create key as movid and corresponding users as a list 
        with open('u.item', 'r', encoding='ISO-8859-1') as movfile: # collect movieids for the movie_genres_and watchers
            for line in movfile:                                    # read each line of the movfile
                movdata = line.split('|')                           # split each information using pipe as they are pipe separated                 
                movid = movdata[0]                                  # get the movie id 
                movtitle = movdata[1]                               # get movie title in the variable which is at position 1 in the line 
                movgenres = []                                      # get genres into the list by looping from position 5 to 23 
                for i in range(5,23):
                    movgenres.append(movdata[i])
                userids = users.get(movid)                          #get the list of userids who have watched the selected movie               
                movie_genres_and_watchers.setdefault(movid, {})     #populare movies dictoinary with the title as key and passing movie genres and userids as the dictionary
                values = {'genre': movgenres, 'userids':userids, 'title':movtitle}
                movie_genres_and_watchers[movid] = values           
    except IOError as ioerr:
            print('File error: ' + str(ioerr))
    except Exception as e:  
            print(str(e.args))
    return movie_genres_and_watchers

# read the external user file and load the information in the structured way to the data dictionary 
def load_usersdetails():
    # set the empty dictionaries
    movies = {}
    user_preference = {}

    # collect movie titles for the movies dictionary
    with open('u.item','r', encoding = 'ISO-8859-1') as movie_file:            
        # sort the file line by line
        for line in movie_file:
            # split the file with the delimeter
            data = line.split('|')
            movie_id = data[0]
            movie_title = data[1]
            # set the dictionary so id is the index and title is related to the index
            movies[movie_id] = movie_title
            
    # split the u.data file into user_preference dictionary
    with open('u.data','r', encoding = 'ISO-8859-1') as user_file:
           
        # sort the file line by line
        for line in user_file:
            # split file and set to variables
            (user_id, movie_id, rating, timestamp) = line.split('\t')[0:4]
            
            # set the nested dictionary
            user_preference.setdefault(user_id, {})
            
            # define the nested dictionary
            user_preference[user_id][movie_id] = [float(rating), movies[movie_id]]
    return user_preference

# map genre positions with the genre name via means of dictionary 
def load_genredetails():
     genredict = {}
     try:
         with open('u.genre', 'r') as genrefile:
             for line in genrefile:
                 words = line.rstrip('\n').split('|')[0:2]
                 if(len(words) != 0 and len(words) != 1):
                     pos = words[1]
                     name = words[0]
                     genredict[pos] = name   
     except:
         print("Issue in reading the external genre file. Either file is not present in the current directory or file might be corrupt!")
     finally:
        return genredict 

# by using this function user can fetch the different genres for the particular movie id 
def fetch_genresformovie(movdict, genredict, movid):
    genres =  [] # container which contain the genres for movid passed in function here
    gencodelist = [] # declare a variable to store passed movie id genres' codes 
    genrenamelist = [v for v in genredict.values()] # populate each values in a sequence inside a list

    # if key present in the movie dictionary, only than search for the genres  
    if(movid in movdict.keys()):
        gencodelist = movdict[movid]['genre'] # put all the passed movie id genres' codes to a temporary variable

    # loop through all the genre code for the passed movie id 
    index = 0 
    for val in gencodelist: 
        if(val == '1'):
            genres.append(genrenamelist[index]) # store the genres names for all the index where genre code is 1 inside genrenamelist list
        index += 1

    return genres # return genres 


