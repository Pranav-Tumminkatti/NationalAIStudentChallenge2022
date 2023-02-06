from flask import Flask, render_template, request, url_for, redirect
from ScenticGCNfunc import has_negative_sentiment
from reddit_scraper_2 import reddit_scraper_via_url, reddit_scraper_via_query
from EmotionalEntailmentFunc import checkemotionalentailment


#add func to return comments list of lists for a post in query

class Comment(object):
    def __init__(self, comment_id, comment_parent, comment_body, comment_link_id, comment_author):
        #find way to change replyto.user @ into "you"
        self.comment_id = comment_id
        self.comment_author = comment_author
        self.comment_parent = comment_parent
        self.comment_link_id = comment_link_id

        edittext = comment_body.split(' ')
        newtext = ''
        for i in edittext:
            if i[:2] == "u/":
                i = 'you'
            newtext += i
            newtext += ' '

        #check if user replying to own comment
        if comment_parent != None:
            if comment_parent.comment_author == comment_author:
                newtext = self.comment_parent.comment_body + ' ' + newtext
                self.comment_parent = comment_parent.comment_parent
        
        self.comment_body = newtext
    
    def cybercheck(self):
        pronouns = set(["you", "him", "she", "they", "your", "youre"])
        if len(set(self.comment_body.split(' ')).intersection(pronouns))==0:
            return False
        elif has_negative_sentiment(self.comment_body):
            #comment has negative sentiment, may be cyberbullying
            if self.comment_parent == None:
                return (True)
            else:
                print("OKAY")
                evidence_utterance = self.create_emotionmodel_input()
                hist = ''
                for evidence in evidence_utterance:
                    hist += evidence + ' '
                target_utterance = [self.comment_body for i in range(len(evidence_utterance))]
                conversation_history = [hist for i in range(len(evidence_utterance))]
                #print(target_utterance,evidence_utterance,conversation_history)
                #return False
                return checkemotionalentailment(target_utterance,evidence_utterance,conversation_history)
        return False
    
    def create_emotionmodel_input(self):
        if self.comment_parent != None:
            lis = self.comment_parent.create_emotionmodel_input()
            lis.extend([self.comment_body])
            return lis
        return [self.comment_body]



def checkdata(post_data, comment_data):
    issues = {}
    for i in range(len(post_data)): #for every post
        post = post_data[i]
        comments = comment_data[i]
        issues[post['id'][0]] = []

        comment_objects = []
        for c in range(len(comments["comment_id"])):
            cparentid = comments["comment_parent_id"][c]
            cparent = ''
            if cparentid != post['id'][0]:
                if cparentid == newcomment.comment_id:
                    cparent = newcomment
                else:
                    for comment in comment_objects:
                        if comment.comment_id == cparentid:
                            cparent = comment
                            break
            if cparent == '':
                cparent = None
            
            try:
                print(comments["comment_id"][c], cparent, comments["comment_body"][c], comments["comment_link_id"][c], comments["comment_author"][c].name)
                newcomment = Comment(comments["comment_id"][c], cparent, comments["comment_body"][c], comments["comment_link_id"][c], comments["comment_author"][c].name)
            except:
                newcomment = Comment(comments["comment_id"][c], cparent, comments["comment_body"][c], comments["comment_link_id"][c], '')
            if newcomment.cybercheck():
                issues[post['id'][0]].append(newcomment)
    print("DONE")
    return issues

#data = reddit_scraper_via_url("https://www.reddit.com/r/cepeeps/comments/10u5pq8/hi/?sort=new")
#print(checkdata(data[0], data[1]))

#thisc = Comment("aa7nl", None, "screw you","aa7asdnl","Ambystom")
#thisc2 = Comment("aa7n2l", thisc, "no screw you","aa72asdnl","asd")
#thisc3 = Comment("aa7n2l", thisc2, "i hate you","aa72asdnl","Ambystom")
#print(thisc3.create_emotionmodel_input())