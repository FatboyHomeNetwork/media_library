
################################################################################################
#
# tokeniser. strings are converted into domain tokens. 
#
################################################################################################

class token(object):
    
    value = ''
    
    def __init__(self, *value):
        
        if len(value) > 0:
            self.value = value[0]
        else:
            self.value = ('')

    def as_string(self):
        if len(self.value) > 0:
            return self.value[0].strip()
        else:
            return ''
    
    def debug_string(self):
        if len(self.value) > 0:
            return self.__class__.__name__ + ': ' + self.value[0].strip()
        else:
            return self.__class__.__name__

class title_token(token):
    def __init__(self, *value):
        super().__init__(value)
    
class year_token(token):
    def __init__(self, *value):
        super().__init__(value)

class season_token(token):
    def __init__(self, *value):
        super().__init__(value)
        
class episode_token(token):
    def __init__(self, *value):
        super().__init__(value)
        
class ext_token(token):
    def __init__(self, *value):
        super().__init__(value)

class domain_number_token(token): 
    def __init__(self, *value):
        super().__init__(value)

class string_token(token):
    def __init__(self, *value):
        super().__init__(value)

import re

class tokeniser(object):
    
    def __as_token(s):
        
        from datetime import date
        
        # year eg 1988
        if len(s) == 4 and s.isdecimal() and int(s) >= 1900 and int(s) <= date.today().year + 1: 
            return [year_token(s)]

        ## Sea & Ep 
        season_pattern = re.compile(r'(season|s)\s*[0-9]{1,3}',flags=re.IGNORECASE) 
        episode_pattern = re.compile(r'(episode|e|part)\s*[0-9]{1,3}',flags=re.IGNORECASE)
        
        number_pattern = re.compile('[0-9]{1,3}')
        
        season_episode = []
        
        season_match = season_pattern.search(s)
        if season_match:
            season_episode.append(season_token())
            season_episode.append(domain_number_token(int(number_pattern.search(season_match.group()).group())))
    
        episode_match = episode_pattern.search(s)
        if episode_match:
            season_episode.append(episode_token())
            season_episode.append(domain_number_token(int(number_pattern.search(episode_match.group()).group())))
            
        if season_match or episode_match:
            return season_episode

        # A domain number should only be an episode, season or sequel number. 
        if len(s) <= 3 and s.isdecimal() and int(s) <= 370: # one episode per day for year plus a few extra. 
## TODO Simple roman numerals. I, II, III, IV, V, VI. Convert to number values              
            return [domain_number_token(str(int(s)))]  
        
        # file ext. will only look for std ext used on the Fatboy Home Network (tm) because the any media we're processes has already been converted, hence is one of the know types 
        if len(s) == 3 and (s.lower() == 'jpg' or s.lower() == 'mp4' or s.lower() == 'mp3' or s.lower() == 'txt'):
            return [ext_token(s)]

        # anything else is a string
        if len (s) > 0:
            return [string_token(s)]
        
        return []

    def tokenise(value):

        elements = [] 
        s = ''
        
## TODO this loop is a bit shit. rework to remove duplicate code & optimise calls to __as_token()
        for c in value:
            if c.isalpha() or c.isnumeric() or c == "\'": 
                s = s + c
            
            else: # is a white space, so end of a token
                if len(s) > 0:
                    elements.append(tokeniser.__as_token(s))
                    s = ''
        
        # pick up the last element
        if len(tokeniser.__as_token(s)) > 0:
            elements.append(tokeniser.__as_token(s))
    
        return elements 
    

################################################################################################
#
# Parsing. This is where we apply the very simple rules for how the language works tot he tokens
#
################################################################################################
class parser(object):

    def parse_season_episode_numbers(elements):
        #
        # <episode> <domain number>
        # <season> <domain number>
        #
        
        rtn = []
        i = 0 
        
        while(True):
            
            if i + 1 > len(elements): 
                break;
            
            if isinstance(elements[i], season_token) and isinstance(elements[i+1], domain_number_token):
                rtn.append(season_token(elements[i+1].value[0]))
                i = i + 1 # eat the domain number token    
                
            elif isinstance(elements[i], episode_token) and isinstance(elements[i+1], domain_number_token): 
                rtn.append(episode_token(elements[i+1].value[0]))
                i = i + 1 # eat the domain number token    
            
            else:
                rtn.append(elements[i])
            
            i = i + 1
            
        return rtn

    def parse_domain_numbers_to_string(elements):
        # any domain_numbers have not been used for se or ep numbers, so they can be used as strings in 
        # title. duplicate domain_numbers, so they can be picked up in titles, but also kept as domain number 
        # tokens to support reasoning 
      
        rtn  = []
        
        for e in elements:
            if isinstance(e, domain_number_token):
                rtn.append(string_token(e.value[0]))
            
            rtn.append(e)
                
        return rtn

    def parse_season_episode_tokens_to_string(elements):
        # any second season or episode token is assumed to be part of a title or description 
        # and convert back to a string token
        
        # rule: only the first season or episode token should be used as the season or episode value. 
        
        rtn = []
        
        first_episode_found = False 
        first_season_found = False 
        
        for e in elements:
            
            if isinstance(e, episode_token):
                if not first_episode_found:
                    rtn.append(e)    
                    first_episode_found = True
                else:
                    rtn.append(string_token(e.value[0]))    
            
            elif isinstance(e, season_token):
                if not first_season_found:
                    rtn.append(e)    
                    first_season_found = True
                else:
                    rtn.append(string_token(e.value[0]))    
            else:
                rtn.append(e)    

        return rtn

    def parse_strings_to_title_one(elements):
        #    
        # <string>* <number> (title 1) | <year> | <ep> | <se> | <string>* <number> (title 2) | <ext>
        # <string>* <number> (title 1) | <year> | <ep> | <se> | <ext> 
        # <string>* <number> (title 1) | <year> | <ext>
        # <string>* <number> (title 1)
        #
        
        title = None
        title_str = ''
        
        rtn = elements.copy()
        
        for e in elements:
            if isinstance(e, string_token):
                title_str += e.as_string().strip() + ' ' 
                rtn.remove(e) # eat strings
            elif isinstance(e, year_token) or isinstance (e, season_token) or isinstance(e, episode_token) or isinstance(e, ext_token):
                title = title_token(title_str.strip())
                rtn.insert(0, title) # insert strings as title
                return rtn
        
        title = title_token(title_str.strip())
        rtn.insert(0, title) # insert strings as title

        return rtn

    def parse_strings_to_title_two(elements):
        #    
        # <string>* <number> (title 1) | <year> | <ep> | <se> | <string>* <number> (title 2) | <ext>
        # <string>* <number> (title 1) | <year> | <ep> | <se> | <ext> 
        # <string>* <number> (title 1) | <year> | <ext>
        # <string>* <number> (title 1)
        #
        
        title = None
        title_str = ''
        
        rtn = elements.copy()
        
        for e in elements:
            if isinstance(e, string_token):
                title_str += e.as_string().strip() + ' ' 
                rtn.remove(e) # eat strings
        
        if len(title_str.strip()) > 0:
            title = title_token(title_str.strip())
            rtn.append(title) 
        
        return rtn
    
################################################################################################
#
# decoder -- entry point for the decode activity
#
################################################################################################

class decoder(object):
        
    def decode(src_string):

        elements = tokeniser.tokenise(src_string)
        
        ## adding domain numbers to season_episode tokens 
        season_episode = parser.parse_season_episode_numbers(elements)
        
        domain_numbers_to_string = parser.parse_domain_numbers_to_string(season_episode)
        season_episode_tokens_to_string = parser.parse_season_episode_tokens_to_string(domain_numbers_to_string)
        
        strings_to_title_one = parser.parse_strings_to_title_one(season_episode_tokens_to_string)
        strings_to_title_two = parser.parse_strings_to_title_two(strings_to_title_one)
        
        return strings_to_title_two
        