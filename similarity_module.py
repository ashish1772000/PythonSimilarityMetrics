#######################################################
# 
# similarity_module.py
# Implementation of the Similarity module
# Author:          Ashish Garg
# Created on:      22-Nov-2019 18:17:53
# 
#######################################################

import math
import utility_module as utils

  
def get_user_vectors(usrpref, usrid1, usrid2):
    vect_container = {}
    vect1 = []
    vect2 = []
    for movie in usrpref[usrid1]:
            if movie in usrpref[usrid2]:
                rating_usr01 = float(usrpref[usrid1][movie][0])
                rating_usr02 = float(usrpref[usrid2][movie][0])

                vect1.append(rating_usr01)
                vect2.append(rating_usr02)
                
    values = {'vect1': vect1, 'vect2':vect2}
    vect_container.update(values)
    return vect_container

def euclidean_similarity(usrpref, usrid1, usrid2):
    vect_containner = get_user_vectors(usrpref, usrid1,usrid2)
    simval = process_euclidean_similarity(vect_containner['vect1'], vect_containner['vect2'])
    return simval
def cosine_similarity(usrpref, usrid1, usrid2):
    vect_containner = get_user_vectors(usrpref, usrid1,usrid2)
    simval = process_cosine_similarity(vect_containner['vect1'], vect_containner['vect2'])
    return simval
def pearson_similarity(usrpref, usrid1, usrid2):
    vect_containner = get_user_vectors(usrpref, usrid1,usrid2)
    simval = process_pearson_similarity(vect_containner['vect1'], vect_containner['vect2'])
    return simval
def jaccard_similarity(usrpref, usrid1, usrid2):
    vect_containner = get_user_vectors(usrpref, usrid1,usrid2)
    simval = process_jaccard_similarity(vect_containner['vect1'], vect_containner['vect2'])
    return simval
def manhattan_similarity(usrpref, usrid1, usrid2):
    vect_containner = get_user_vectors(usrpref, usrid1,usrid2)
    simval = process_manhatten_similarity(vect_containner['vect1'], vect_containner['vect2'])
    return simval

def get_movie_vectors(movgenreandwatchers, movid1, movid2, simfunc):
    # populate vector1 and vector2 with the genres movies belong to 
    vect1 = movgenreandwatchers[movid1]['genre'] 
    vect2 = movgenreandwatchers[movid2]['genre']

    if(simfunc == utils.sim_func_code.JACCARD):
       vect1 = [index for index, genre in enumerate(vect1) if genre == '1'] # Create new set with positions where 1 appears 
       vect2 = [index for index, genre in enumerate(vect2) if genre == '1']
    
    return [vect1, vect2]

def find_movie_similarity(usrpref, movgenreandwatchers, title1, title2, simfunc):
    similarity_index_genre = 0
    similarity_index_ratings = 0

    # first step is to retrieve the respective ids from the titles
    movid1 = [str(movid) for movid, movdetails in movgenreandwatchers.items() if movdetails['title'] == title1] #retrieve movie id 1 from title 1
    movid2 = [str(movid) for movid, movdetails in movgenreandwatchers.items() if movdetails['title'] == title2] #retrieve movie id 2 from title 2

    # movid returns list and hence to return string need to take first index from the list as movid1[0] and same for movid2
    movid1 =movid1[0]
    movid2 = movid2[0]

    # get two vectors based on the genres similarity between two movies 
    vectors_movie_genres = get_movie_vectors(movgenreandwatchers, movid1, movid2, simfunc) 

    # get two vectors based on the common watchers for two movies's ratings 
    vectors_common_watchers_ratings = get_common_watchers_ratings(movid1, movid2, movgenreandwatchers, usrpref) 
   
    # populate genres vectors locally
    vect1_genre = vectors_movie_genres[0]
    vect2_genre = vectors_movie_genres[1] 

    # populate ratings' vectors locally
    vect1_rating = vectors_common_watchers_ratings[0]
    vect2_rating = vectors_common_watchers_ratings[1]

    # based on the selected function call the respective similarity function
    if(simfunc == utils.sim_func_code.EUCLIDEAN):
        similarity_index_genre = process_euclidean_similarity(vect1_genre, vect2_genre)
        similarity_index_ratings = process_euclidean_similarity(vect1_rating, vect2_rating)
    elif(simfunc == utils.sim_func_code.COSINE):
        similarity_index_genre = process_cosine_similarity(vect1_genre, vect2_genre) 
        similarity_index_ratings = process_cosine_similarity(vect1_rating, vect2_rating)
    elif(simfunc == utils.sim_func_code.PEARSON):
        similarity_index_genre = process_pearson_similarity(vect1_genre, vect2_genre)     
        similarity_index_ratings = process_pearson_similarity(vect1_rating, vect2_rating)
    elif(simfunc == utils.sim_func_code.JACCARD):
        similarity_index_genre = process_jaccard_similarity(vect1_genre, vect2_genre) 
        similarity_index_ratings = process_jaccard_similarity(vect1_rating, vect2_rating)
    elif(simfunc == utils.sim_func_code.MANHATTAN):
        similarity_index_genre = process_manhatten_similarity(vect1_genre, vect2_genre)  
        similarity_index_ratings = process_manhatten_similarity(vect1_rating, vect2_rating)
    else:
        similarity_index_genre = process_cosine_similarity(vect1_genre, vect2_genre)
        similarity_index_ratings = process_cosine_similarity(vect1_rating, vect2_rating)
    
    weight_for_genres = 0.8
    weight_for_rating = 0.2

    total_movie_similarity_index = ((weight_for_genres * similarity_index_genre) + (weight_for_rating * similarity_index_ratings))
    return round(total_movie_similarity_index,1)

def process_pearson_similarity(vect1, vect2):
    corr_coeff = 0    
    try:
        #convert values in vect1 from string to int so can perform arithmatic cumulative operations like sum
        vect1 = [int(val) for val in vect1]
        vect2 = [int(val) for val in vect2]

        #take the mean of both the vectors 
        avg_vect01 = sum(vect1)/len(vect1) 
        avg_vect02 = sum(vect2)/len(vect2) 

        #calculate each value (e.g. rating) from the mean value (e.g. mean rating) for both the vectors 
        distfromavg_vect01 = [round(float(val) - avg_vect01, 3) for val in vect1]
        distfromavg_vect02 = [round(float(val) - avg_vect02, 3) for val in vect2]

        #vector 1 and vector 2 combined 
        sumof_productof_vectdists = sum([float(val1) * float(val2) for val1, val2 in zip(distfromavg_vect01, distfromavg_vect02)])

        #take the square root of sum of squares of distances from the respective means for each vectors
        sumof_sqrof_distfromavg_vect01 = math.sqrt(sum([pow(float(val),2) for val in distfromavg_vect01]))
        sumof_sqrof_distfromavg_vect02 = math.sqrt(sum([pow(float(val),2) for val in distfromavg_vect02]))

        #combine both the square root distances to one 
        productof_sumof_sqrof_distfromavg_ofvect1andvect2 = (sumof_sqrof_distfromavg_vect01 * sumof_sqrof_distfromavg_vect02)

        if productof_sumof_sqrof_distfromavg_ofvect1andvect2 == 0:
            return 0
        else:
            #finally get the value of combined mean distance of vectors by combined square root distance of vectors to find the correlation coefficient 
            corr_coeff = sumof_productof_vectdists/productof_sumof_sqrof_distfromavg_ofvect1andvect2
            return round(corr_coeff, 3)
    except:
        print("Somthing wrong with the pearson correlation calculation. Check the values passed!")    

def process_jaccard_similarity(vect1, vect2):
    v1 = set(vect1)
    v2 = set(vect2)

    # store count of common numbers present in both the sets by intersecting vectors
    numr = len(v1.intersection(v2))

    # store count of numbers present in either sets
    denomtr = len(v1.union(v2))

    jacvalue = numr/denomtr
    return round(jacvalue,3)

def process_manhatten_similarity(vect1,vect2):
    try:
        v1_v2 =  [abs(float(v1) - float(v2)) for v1, v2 in zip(vect1, vect2)]
        mandist = sum(v1_v2)
        man_simindex = 1/(1+mandist)
    except ZeroDivisionError:
        man_simindex = math.nan
    finally:
        return round(man_simindex, 3)

def process_euclidean_similarity(vect1, vect2):
    try:
        v1_v2 = [float(v1)-float(v2) for v1, v2 in zip(vect1, vect2)]
        sq_v1_v2 = [float(v) * float(v) for v in v1_v2]
        euc_dist = math.sqrt(sum(sq_v1_v2))
        euc_similarity = 1/(1+euc_dist)
    except ZeroDivisionError:    
        euc_similarity = math.nan            
    finally:
        return round(euc_similarity,3)

def process_cosine_similarity(vect1, vect2):
    try:
        v1v2 = [float(val1) * float(val2) for val1, val2 in zip(vect1,vect2)]
        v1v1 = [float(val1) * float(val1) for val1 in vect1]
        v2v2 = [float(val2) * float(val2) for val2 in vect2]
        cossimilarity = sum(v1v2)/(math.sqrt(sum(v1v1)) * math.sqrt(sum(v2v2)))
        #cosdistance = 1 - cossimilarity
    except ZeroDivisionError:    
        cossimilarity = math.nan  
    finally:
        return round(cossimilarity,3)
              
def get_common_watchers_ratings(movid1, movid2, movie_genres_and_watchers, usrpref):
    common_watchers = set(movie_genres_and_watchers[movid1]['userids']).intersection(set(movie_genres_and_watchers[movid2]['userids']))
    count_common_watchers = len(common_watchers)
    
    rating_vect1 = []
    for uid in common_watchers:
        rat = [movdetails[0] for movid, movdetails in usrpref[uid].items() if movid == movid1]
        rating_vect1.append(rat[0])
    
    rating_vect2 = []
    for uid in common_watchers:
        rat = [movdetails[0] for movid, movdetails in usrpref[uid].items() if movid == movid2]
        rating_vect2.append(rat[0])

    return [rating_vect1, rating_vect2]



