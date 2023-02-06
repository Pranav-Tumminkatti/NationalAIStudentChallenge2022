#######
# IMPORT PACKAGES
#######

import praw
import pandas as pd


# Acessing the reddit api
def reddit_scraper_via_url(url):
    reddit = praw.Reddit(client_id="aQ8y8McfRW1pqeVd1UQ2kw",         # your client id
                        client_secret="Y8xnFSJFGExOmlbNekoUAJY1KN0Xlw",      # your client secret
                        user_agent="webscraper")     # user agent name
    
    submission = reddit.submission(url=url)
    
    post_dict = {
        "title" : [],
        "score" : [],
        "id" : [],
        "url" : [],
        "comms_num": [],
        "created" : [],
        "body" : []
    }
    comments_dict = {
        "comment_id" : [],
        "comment_parent_id" : [],
        "comment_body" : [],
        "comment_link_id" : [],
        'comment_author' : []
    }
    
    post_dict["title"].append(submission.title)
    post_dict["score"].append(submission.score)
    post_dict["id"].append(submission.id)
    post_dict["url"].append(submission.url)
    post_dict["comms_num"].append(submission.num_comments)
    post_dict["created"].append(submission.created)
    post_dict["body"].append(submission.selftext)
    
    ##### Acessing comments on the post
    submission.comments.replace_more(limit = 1)
    for comment in submission.comments.list():
        comments_dict["comment_id"].append(comment.id)
        comments_dict["comment_parent_id"].append(comment.parent().id)
        comments_dict["comment_body"].append(comment.body)
        comments_dict["comment_link_id"].append(comment.link_id)
        comments_dict["comment_author"].append(comment.author)
    
    post_comments = pd.DataFrame(comments_dict)
    post_comments.to_csv('csv/'+str(post_dict['title'][0]) +"__comments__.csv")
    post_data = pd.DataFrame(post_dict)
    post_data.to_csv('csv/'+str(post_dict['title'][0]) +"__info__.csv")
    
    return [post_dict],[comments_dict]
    

def reddit_scraper_via_query(sub=['Askreddit'], query=['Coding'],sort='top',limit=1):
    reddit = praw.Reddit(client_id="aQ8y8McfRW1pqeVd1UQ2kw",         # your client id
                        client_secret="Y8xnFSJFGExOmlbNekoUAJY1KN0Xlw",      # your client secret
                        user_agent="webscraper")     # user agent name
    
    info_res = []
    comments_res = []

    for s in sub:
        subreddit = reddit.subreddit(s)   # Chosing the subreddit
        
    ########################################
    #   CREATING DICTIONARY TO STORE THE DATA WHICH WILL BE CONVERTED TO A DATAFRAME
    ########################################

    #   NOTE: ALL THE POST DATA AND COMMENT DATA WILL BE SAVED IN TWO DIFFERENT
    #   DATASETS AND LATER CAN BE MAPPED USING IDS OF POSTS/COMMENTS AS WE WILL 
    #   BE CAPTURING ALL IDS THAT COME IN OUR WAY

    # SCRAPING CAN BE DONE VIA VARIOUS STRATEGIES {HOT,TOP,etc} we will go with keyword strategy i.e using search a keyword

        for item in query:
            post_dict = {
                "title" : [],
                "score" : [],
                "id" : [],
                "url" : [],
                "comms_num": [],
                "created" : [],
                "body" : []
            }
            comments_dict = {
                "comment_id" : [],
                "comment_parent_id" : [],
                "comment_body" : [],
                "comment_link_id" : [],
                'comment_author' : []
            }
            for submission in subreddit.search(item,sort=sort,limit = int(limit)):
                post_dict["title"].append(submission.title)
                post_dict["score"].append(submission.score)
                post_dict["id"].append(submission.id)
                post_dict["url"].append(submission.url)
                post_dict["comms_num"].append(submission.num_comments)
                post_dict["created"].append(submission.created)
                post_dict["body"].append(submission.selftext)
                
                ##### Acessing comments on the post
                submission.comments.replace_more(limit = 1)
                for comment in submission.comments.list():
                    comments_dict["comment_id"].append(comment.id)
                    comments_dict["comment_parent_id"].append(comment.parent().id)    #comment.parent_id or comment.parent().id?
                    comments_dict["comment_body"].append(comment.body)
                    comments_dict["comment_link_id"].append(comment.link_id)
                    comments_dict["comment_author"].append(comment.author)
            
            post_comments = pd.DataFrame(comments_dict)
            post_comments.to_csv('csv/'+s+"_comments_"+ item +"subreddit.csv")
            post_data = pd.DataFrame(post_dict)
            post_data.to_csv('csv/'+s+"_info_"+ item +"subreddit.csv")
            
            info_res.append(post_dict)
            comments_res.append(comments_dict)

    return info_res, comments_res

if __name__ == '__main__':
    #info,comments = reddit_scraper_via_query()
    #print(info)
    
    #info,comments = reddit_scraper_via_url('https://www.reddit.com/r/cepeeps/comments/10u5pq8/hi/')
    
    info,comments = reddit_scraper_via_query(['InterestingAsFuck'],['Water'],'top',2)
    

'''
Reddit test URLs:
1. https://www.reddit.com/r/askSingapore/comments/10tbdsc/missing_phone/
2. https://www.reddit.com/r/cepeeps/comments/10u5pq8/hi/

'''

'''
Okay the syntax for querying the reddit data is as follows:

info_list --> info[_postnumber][field_][0]
Example: info[0]['title'][0]  (gets the title of the first post)

comments_list --> comments[_postnumber][field][commentnumber_]
Example: comments[0]['id'][11] (gets the id of the 11th comment on the first post
'''