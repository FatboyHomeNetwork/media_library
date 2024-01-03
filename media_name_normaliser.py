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
            self.value = ''

    def __str__(self):
        if len(self.value) > 0:
            return self.__class__.__name__ + ': ' + self.value[0].strip()
        else:
            return self.__class__.__name__

    def as_string(self):
        if len(self.value) > 0:
            return self.value[0].strip()
        else:
            return ''

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


class tokeniser(object):
    
    def __token_factory(s):
        
        from datetime import date
        
        # year eg 1988
        if len(s) == 4 and s.isdecimal() and int(s) >= 1900 and int(s) <= date.today().year + 1: 
            return [year_token(s)]

        # normalised seasion & episode eg S03E12
        if len(s) == 6 and s[0].lower() == 's' and s[2:3].isdecimal() and s[3:4].lower() == 'e' and s[5:6].isdecimal(): 
            return [season_token(), domain_number_token(str(int(s[2:3]))), episode_token(), domain_number_token(str(int(s[5:6])))]

        # normalised seasion eg S01
        if len(s) == 3 and s[0].lower() == 's' and s[2:3].isdecimal(): 
            return [season_token(), domain_number_token(str(int(s[2:3])))]
        
        # normalised episode eg E12
        if len(s) == 3 and s[0].lower() == 'e' and s[2:3].isdecimal(): 
            return [episode_token(), domain_number_token(str(int(s[2:3])))]
        
        # free form seasion eg: Season: 1 |  s 01 
        if s.lower() == 'season' or s.lower() == 's':  
            return [season_token(s)]
    
        # free form episode eg: episode 1 |  e 01 | part 3
        if s.lower() == 'episode' or s.lower() == 'e' or s.lower() == 'part': 
            return [episode_token(s)]
            
        # A domain number should only be an episode, season or sequal number. 
        if len(s) <= 3 and s.isdecimal() and int(s) <= 370: # one episode per day for year plus a few extra. 
            return [domain_number_token(str(int(s)))]  
        
        # file ext. will only look for std ext used on the Fatboy Home Network (tm)
        if len(s) == 3 and (s.lower() == 'jpg' or s.lower() == 'mp4' or s.lower() == 'mp3' or s.lower() == 'txt'):
            return [ext_token(s)]

        # anthing else is a string
        if len (s) > 0:
            return [string_token(s)]
        
        return []


    def tokenise(value):

        elements = [] 
        s = ''
        
        for c in value:
            if c.isalpha() or c.isnumeric():
                s = s + c
            
            else: # is a white space, so end of a token
                if len(s) > 0:
                    for e in tokeniser.__token_factory(s):
                        elements.append(e)
                    s = ''
        
        # pick up the last element
        if len(tokeniser.__token_factory(s)) > 0:
            elements.append(tokeniser.__token_factory(s)[0]) 
    
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

    def parse_strings_to_titles(elements):
        #    
        # <string>* <number> (title 1) | <year> | <ep> | <se> | <string>* <number> (title 2) | <ext>
        # <string>* <number> (title 1) | <year> | <ep> | <se> | <ext> 
        # <string>* <number> (title 1) | <year> | <ext>
        # <string>* <number> (title 1)
        #
        
        # title 1
        title_one = None
        title_str = ''
        
        for e in elements:
            if isinstance(e, year_token) or isinstance (e, season_token) or isinstance(e, episode_token) or isinstance(e, ext_token):
                if len(title_str) > 0:
                    title_one = title_token(title_str.strip())
                break
            
            else:
                title_str = title_str + e.as_string() + ' ' 
        
        if title_one == None and len(title_str.strip()) > 0: # special case of a string only element
            title_one = title_token(title_str.strip())
            
        # title 2
        title_two = None
        title_str = ''
        ext = None
        
        elements.reverse()
        
        for e in elements:
            
            if isinstance(e, ext_token):
                ext = ext_token
                continue
            
            if not isinstance (e, string_token):
                if len(title_str) > 0:
                    title_two = title_token(title_str.strip())

            else:
                title_str = e.as_string()  + ' ' +  title_str
        
        elements.reverse()        
        
        # replace the start and end string with the two titles
        rtn = []
        if title_one != None:
            rtn.append(title_one)
        
        for e in elements:
            if not isinstance (e, string_token):
                rtn.append(e)

        if title_two != None:
            rtn.append(title_two)
        
        # add back the extension 
        if ext != None:
            rtn.append(ext)
    
        return rtn
    
################################################################################################
#
# decoder  
#
################################################################################################

class decoder(object):
    
    def __init__(self, path):
        self.__path = path
        
    def decode(self):

        elements = tokeniser.tokenise(self.__path)
        
        elements = parser.parse_season_episode_numbers(elements)
        elements = parser.parse_domain_numbers_to_string(elements)
        elements = parser.parse_season_episode_tokens_to_string(elements)
        elements = parser.parse_strings_to_titles(elements)
        
        return elements


class path_normaliser(object):
    
    def __init__(self, path):
        self.__path = path
        
    def normalise(self): 
        elements = d = decoder(self.__path)
    
        return 'normalised_directory'

        
        
    