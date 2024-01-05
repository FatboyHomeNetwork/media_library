import decoder
from decoder import decoder as dc

################################################################################################
#
# Media Item Domain Model 
#
# This builds a series -> season -> episode model. Series values: title, year,  series numb, 
# episode name and number numb are populated based on explicit and calculated vales. 
#
################################################################################################

#
# abstract media item common class 
#
class abstract_media_item(object):

    def __init__(self, path):
                
        self.exp_media_item_path = path     
        self.cal_normalised_path = None
        
        #self.path = self.exp_media_item_path
        
        self.exp_title_one = None
        self.exp_title_two = None

        self.exp_domain_numbers = []
                
        self.exp_year = None
        self.cal_year = None
        self.det_year = None
        
        self.exp_path_tokens = dc.decode(os.path.basename(self.exp_media_item_path))
        
        for e in self.exp_path_tokens: 
            
            if isinstance(e, decoder.title_token):
                if self.exp_title_one == None: 
                    self.exp_title_one = e.value[0]
                else:
                    self.exp_title_two = e.value[0]
            
            if isinstance(e, decoder.year_token): 
                self.exp_year = e.value[0]
                
            if isinstance(e, decoder.domain_number_token):
                self.exp_domain_numbers.append(e.value[0])

    def __str__(self):
        
        rtn = 'is a: %s\n' % (self.__class__.__name__)
        rtn = '%sexp path: %s\n' % (rtn, self.exp_media_item_path)
        
        rtn = '%sexp title one: %s\n' % (rtn, self.exp_title_one)
        rtn = '%sexp title two: %s\n' % (rtn, self.exp_title_two)
        
        rtn = '%sexp year: %s\n' % (rtn, self.exp_year)
        
        domain_numbers = None
        if len(self.exp_domain_numbers) > 0:
            domain_numbers = ' '.join(self.exp_domain_numbers)
        rtn = '%sexp domain numbers: %s\n' % (rtn, domain_numbers)
        
        return rtn

##################################################
#
# class - Series
#
class series(abstract_media_item):
    
    def __init__(self, model):
        
        super().__init__(model)
        
        self.exp_seasons = []
        
        # title is managed by commmon_item
        self.cal_series_title = None
        self.det_series_title = None
        
        # populate seasons
        natural_collection_position = 1
        
        for p in model:
            self.exp_seasons.append(season(p),natural_collection_position)
            natural_collection_position = natural_collection_position + 1

        # calculate fields 
        self.cal_year = self.calulate_series_year()
        self.det_year = self.determine_series_year()
        
        self.cal_series_title = self.calulate_series_title()
        self.det_series_title = self.determine_series_title()
        
        # tell my seasons my determined year and title 
        for s in self.exp_seasons:
            s.set_determine_series_year(self.det_year) 
            s.set_determine_series_title(self.det_series_title)

    def __str__(self):
        rtn = '%scal series title: %s\n' % (super().__str__(), self.cal_series_title)
        rtn = '%sdet series title: %s\n' % (rtn, self.det_series_title)
        
        rtn = '%scal series year: %s\n' % (rtn, self.cal_year)
        rtn = '%sdet series year: %s\n' % (rtn, self.det_year)
 
        for s in self.exp_seasons:
            rtn = '%s%s' % (rtn, s)

        return rtn
    
    def normalise(self):
        
        norm_model = [] 
        for s in self.exp_seasons:
             norm_model.append(s.normalise(self.det_series_title))
        return norm_model 
    #
    # Cal functions
    #
    
    def calulate_series_year(self):
        # if AGREEMENT level of season have the same get_calulate_series_year(), then 
        # get_calulate_series_year() becomes cal_series_year
         
        AGREEMENT = .90   
        years = {}
        
        for s in self.exp_seasons:
            get_calulate_series_year = s.get_calulate_series_year() 
            if get_calulate_series_year in years.keys():
                years[get_calulate_series_year] = years[get_calulate_series_year] + 1
            else:
                years[get_calulate_series_year] = 1
           
        import operator
        years = sorted(years.items(), key=operator.itemgetter(1), reverse=True)
        
        if years[0][0] != None and years[0][1] > (len(self.exp_seasons) * AGREEMENT): 
            return years[0][0]
        else:
            return None


    def determine_series_year(self):
        # use exp year if available, then cal year if available. 
        
        if self.exp_year == None:
            return self.cal_year
        else: 
            return self.exp_year

    
    def calulate_series_title(self):
        # if AGREEMENT level of seasion have the same get_calulate_series_title(), then 
        # get_calulate_series_title() becomes cal_series_title
        
        AGREEMENT = .90   
        names = {}
        
        for s in self.exp_seasons:
            name = s.get_calulate_series_title()
            if name in names.keys():
                names[name] = names[name] + 1
            else:
                names[name] = 1
           
        import operator
        names = sorted(names.items(), key=operator.itemgetter(1), reverse=True)
        
        if names[0][0] != None and names[0][1] > (len(self.exp_seasons) * AGREEMENT): 
            return names[0][0]
        else:
            return None

    
    def determine_series_title(self):
        # use cal title if available, else return title 1.
        
        if self.cal_series_title != None:
            return self.cal_series_title
        else:
            return self.exp_title_one
        
##################################################
#
# class - Season
#
class season(abstract_media_item):
    
    def __init__(self, path, pos):
        super().__init__(path)
        
        self.exp_pos = pos
        
        self.exp_season_number = None
        self.det_season_number = None 
        self.cal_season_number = None
        
        self.det_series_year = None
        self.det_series_title = None
        
        # populate self 
        for e in self.exp_path_tokens: 
            if isinstance(e, decoder.season_token):
               self.exp_season_number = e.value[0]
        
        # populate episodes
        self.exp_episodes = []
        
        for p in self.__model:
            self.exp_episodes.append(episode(p), natural_collection_position)
            natural_collection_position = natural_collection_position + 1

        # Set episodes properities based on series and seasion values 
        self.cal_season_number = self.__calulate_season_number()
        self.det_season_number = self.__determine_season_number()

        for e in self.exp_episodes:
            e.set_determine_series_title(self.det_series_title)
            e.set_determine_series_year(self.det_series_year)
            e.set_determine_season_number(self.det_season_number)

        self.__calulate_episodes_title()


    def __str__(self):
        rtn = '%sexp pos: %s\n' % (super().__str__(), self.exp_pos)
        
        rtn = '%sexp season number: %s\n' % (rtn, self.exp_season_number)
        rtn = '%scal season number: %s\n' % (rtn, self.cal_season_number)
        rtn = '%sdet season number: %s\n' % (rtn, self.det_season_number)
        
        for e in self.exp_episodes:
            rtn = '%s%s' %(rtn, e)
        
        return rtn
    
    def normalise(self, normalised_series):
        
        rtn = []
        
        normalised_season = 'Season %s' % self.det_season_number
        normalised_season_path = os.path.join(normalised_series, normalised_season)
        
        for e in self.exp_episodes:
            p =  + e.normalise(normalised_season_path)
            rtn.append(p)
        
        return rtn

    #
    #  series functions - called by series 
    #
    
    def get_calulate_series_title(self):
        # if AGREEMENT level of episodes have the same title_one, then title_one is the this seasion's series title. 
    
        AGREEMENT = .90   
        titles = {}
        
        for e in self.exp_episodes:
            
            if e.exp_title_one != None:
                if e.exp_title_one in titles.keys():
                    titles[e.exp_title_one] =  titles[e.exp_title_one] + 1
                else:
                    titles[e.exp_title_one] = 1
        
        import operator
        titles = sorted(titles.items(), key=operator.itemgetter(1), reverse=True)
        
        if titles[0][1] > (len(self.exp_episodes) * AGREEMENT): 
            return titles[0][0]
        else:
            return None
        

    def get_calulate_series_year(self):
        # if AGREEMENT level of episodes have the same year, then year is seasion's series year. 
    
        AGREEMENT = .90   
        years = {}
        
        for e in self.exp_episodes:
            
            if e.exp_year != None:
                if e.exp_year in years.keys():
                    years[e.exp_year] = years[e.exp_year] + 1
                else:
                    years[e.exp_year] = 1
        
        import operator
        years = sorted(years.items(), key=operator.itemgetter(1), reverse=True)
        
        if len(years) > 0 and years[0][1] > (len(self.exp_episodes) * AGREEMENT): 
            return years[0][0]
        else:
            return None
    
    #
    # episode set functions called by series 
    #
    
    def set_determine_series_year(self, series_year):
        for e in self.exp_episodes:
            e.set_determine_series_year(series_year)
    
    def set_determine_series_title(self, series_title):
        for e in self.exp_episodes:
            e.set_determine_series_title(series_title)
    
    #
    # episode sets functions calcualted by seasons
    #    

    def __calulate_episodes_title(self):
        # sets an episodes title based on the uniquness of title_one and title_two
        # within the season. 
                       
        MAX_DUPLICATES = 2 # better as a % of total set; an agreement level  
        
        title_one = {}
        title_two = {}
        
        title_one_is_unique = False
        title_two_is_unique = False
                
        
        # Count title occurance 
        for e in self.exp_episodes:
            
            if e.exp_title_one != None:
                if e.exp_title_one in title_one.keys():
                    title_one[e.exp_title_one] = title_one[e.exp_title_one] + 1
                else:
                    title_one[e.exp_title_one] = 1
        
            if e.exp_title_two != None:
                if e.exp_title_two in title_two.keys():
                    title_two[e.exp_title_two] =  title_two[e.exp_title_two] + 1
                else:
                    title_two[e.exp_title_two] = 1
        
        
        # determine uniqueness
        if len(title_one) > 0:
            import operator
            title_one = sorted(title_one.items(), key=operator.itemgetter(1), reverse=True)
            
            if title_one[0][1] <= MAX_DUPLICATES:
                title_one_is_unique = True
            else:
                title_one_is_unique = False
            
        if len(title_two) > 0:
            title_two = sorted(title_two.items(), key=operator.itemgetter(1), reverse=True)

            if title_two[0][1] <= MAX_DUPLICATES:
                title_two_is_unique = True
            else:
                title_two_is_unique = False

        
        # uniqueness rules
        if title_one_is_unique == False and title_two_is_unique == True:
            # <series name> <year | Se# | Ep#> <ep name>. 
            
            for e in self.exp_episodes:
                e.set_determine_episode_title__T2()
 
        if title_one_is_unique == True and title_two_is_unique == False:
            # <ep name> <year | Se# | Ep#> <common torrent description or blah> 
            # <ep name> <year | Se# | Ep#> 
            # <ep name> 
            
            for e in self.exp_episodes:
                e.set_determine_episode_title__T1()
 
        if title_one_is_unique == True and title_two_is_unique == True:
            # <ep name?> <year | Se# | Ep#> <descrption?>
            
            for e in self.exp_episodes:
                e.set_determine_episode_title__T1_T2()
            
        if title_one_is_unique == False and title_two_is_unique == False:
            # <collection common string> <year | Se# | Ep#> <collection common string>
            
            for e in self.exp_episodes:
                e.set_determine_episode_title__T1_T2()
    
    
    def __calulate_season_number(self):
        # if AGREEMENT level of episodes have the same season_number, then season_number is season's series season_number. 
    
        AGREEMENT = .90   
        seasons = {}
        
        for e in self.exp_episodes:
            
            if e.exp_season_number != None:
                if e.exp_season_number in seasons.keys():
                    seasons[e.exp_season_number] = seasons[e.exp_season_number] + 1
                else:
                    seasons[e.exp_season_number] = 1
        
        import operator
        seasons = sorted(seasons.items(), key=operator.itemgetter(1), reverse=True)
        
        if seasons[0][1] > (len(self.exp_episodes) * AGREEMENT): 
            return seasons[0][0]
        else:
            return None
    
    def __determine_season_number(self):
        # use explicit season number if it exists, else use calculated season numnber   
        if self.exp_season_number != None:
            return self.exp_season_number.zfill(2)
        else:
            return self.cal_season_number.zfill(2)


##################################################
#
# class - Episode
#
class episode(abstract_media_item):
   
    def __init__(self, path, pos):
        super().__init__(path)
        
        self.exp_pos = pos
        self.exp_ext = None
        
        self.exp_episode_number = None
        self.cal_episode_number = None
        self.det_episode_number = None
        
        self.exp_season_number = None
        self.cal_season_number = None
        self.det_season_number = None
        
        self.det_series_title = None
        
        self.det_episode_title = None
                        
        for e in self.exp_path_tokens:
            if isinstance (e, decoder.episode_token) and self.exp_episode_number == None:
                self.exp_episode_number = e.value[0]

            if isinstance(e, decoder.season_token) and self.exp_season_number == None:
               self.exp_season_number = e.value[0]
               
            if isinstance(e, decoder.ext_token):
                self.exp_ext = e.value[0]

        self.cal_episode_number = self.__calulate_episode_number()
        self.det_episode_number = self.__determine_episode_number()


    def __str__(self):
        rtn = '%sexp pos: %s\n' % (super().__str__(), self.exp_pos)
        
        rtn = '%sdet series title: %s\n' % (rtn, self.det_series_title)
        rtn = '%sdet series year: %s\n' % (rtn, self.det_year)
        
        rtn = '%sdet season number: %s\n' % (rtn, self.det_season_number)
                        
        rtn = '%sexp episode number: %s\n' % (rtn, self.exp_episode_number)
        rtn = '%scal episode number: %s\n' % (rtn, self.cal_episode_number)
        rtn = '%sdet episode number: %s\n' % (rtn, self.det_episode_number)
        
        rtn = '%sdet episode title: %s\n' % (rtn, self.det_episode_title)
        
        rtn = '%sexp ext: %s\n' % (rtn, self.exp_ext)
        
        return rtn

    def normalise(self, head):
        
        # series_title (year) SXXEXX episode_title . ext 
        self.cal_normalised_path = '%s (%s) S%sE%s %s.%s' %(self.det_series_title, self.det_year, self.det_season_number, self.det_episode_number, self.det_episode_title, self.exp_ext)
        
        return os.path.join(head,self.cal_normalised_path)
        
    #
    # Cal & det functions
    #
            
    def __calulate_episode_number(self):
        return self.exp_pos

    def __determine_episode_number(self):
        # if there is no expicit episode number, use calculated episode number
        
        if self.exp_episode_number != None:
            return self.exp_episode_number.zfill(2)
        else:
            return self.cal_episode_number.zfill(2)
    
    #
    # Det functions called by seasion 
    #
    
    def set_determine_series_title(self, title):
        self.det_series_title = title
    
    def set_determine_series_year(self, year):
        self.det_year = year 
        
    def set_determine_season_number(self, number):
        self.det_season_number = number
    
    
    def set_determine_episode_title__T1(self):
        self.det_episode_title = self.exp_title_one
        
    def set_determine_episode_title__T2(self):
        self.det_episode_title = self.exp_title_two
    
    def set_determine_episode_title__T1_T2(self):
        self.det_episode_title = '%s %s' % (self.exp_title_one, self.exp_title_two)

    def set_determine_episode_title__none(self):
        self.det_episode_title = None
    

################################################################################################
#
# Normalise a given media path in to one of the following structures:
#
# <Series Name> (<Year>)            
#     Season <xx> 
#         <Series Name> (<Year>) S<xx> E<xx> <Episode Title> . <extension>  
#
# <Movie Title> (<year>) 
#     <Movie Title> (<year>) . <extension>  
#
################################################################################################



class normaliser(object):
    
    def __init__(self, model):
        self.__model = model
    
    def __contains_series(self, elements):
        
        for e in elements:
            if isinstance(e, decoder.season_token) or isinstance(e, decoder.episode_token): 
                return True
        
        return False
    
    def __is_series(self):
        # if AGREEMENT level of items have series tokens in their names, assume this is a series
        
        AGREEMENT = .90
        
        total_items = 0 
        series_items = 0 

        for p in self.__model:
            #dc = decoder.decoder()
            if self.__contains_series(dc.decode(p)):
                series_items = series_items + 1
            total_items = total_items + 1
            
        if series_items >= total_items * AGREEMENT:
            return True
        else:
            return False
   
    def normalise(self):
        
        norm_path_model = None
        
        media_item = series(self.__model)
        norm_path_model = media_item.normalise()
        norm_path_model = media_item.cal_normalised_path
        norm_path_model = self.__model.copy()            
        
        return norm_path_model


################################################################################################
#
# Module support functions 
#
################################################################################################

import os

def create_path_model(src_path):
    
    path_model = []
    
    if os.path.exists(src_path) and os.path.isdir(src_path):
        for subdir, dirs, files in os.walk(src_path):
            for f in files:
                p = os.path.join(subdir, f)
                path_model.append(p)
    
    return path_model