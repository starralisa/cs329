# ========================================================================
# Copyright 2021 Emory University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========================================================================
import re

def normalize(text):

    RE_main = re.compile(r'(?i)(((ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)|(one|two|three|four|five|six|seven|eight|nine)|(hundred|thousand|million|billion|trillion))[ -]*)+')
    RE_ones = re.compile(r'(?i)(?s:.*)((one)|(two)|(three)|(four)|(five)|(six)|(seven)|(eight)|(nine))([ -]*)')
    RE_ones_forward = re.compile(r'(?i)((one)|(two)|(three)|(four)|(five)|(six)|(seven)|(eight)|(nine))([ -]*)')
    RE_tens = re.compile(r'(?i)((twenty)|(thirty)|(forty)|(fifty)|(sixty)|(seventy)|(eighty)|(ninety))([ -]*)')
    RE_hundred = re.compile(r'(?i)(hundred)([ -]*)')
    RE_pos = re.compile(r'(?i)((thousand)|(million)|(billion)|(trillion))([ -]*)')
    RE_pos_no_spaces = re.compile(r'(?i)(thousand)|(million)|(billion)|(trillion)')
    RE_teens = re.compile(r'(?i)((ten)|(eleven)|(twelve)|(thirteen)|(fourteen)|(fifteen)|(sixteen)|(seventeen)|(eighteen)|(nineteen))([ -]*)')
    RE_ones_hundred = re.compile(r'(?i)((one)|(two)|(three)|(four)|(five)|(six)|(seven)|(eight)|(nine))([ -]*)(hundred)')
    RE_space = re.compile(r'[\s-]+')
    RE_word_char_before_following_space = re.compile(r'((\w)[ -]+)$')
    RE_decimal = re.compile(r'(?i)((ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|one|two|three|four|five|six|seven|eight|nine|hundred|thousand|million|billion|trillion)[ -]*)*(point)([ -]*(ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|one|two|three|four|five|six|seven|eight|nine|hundred|thousand|million|billion|trillion))*')
    RE_fractional_or_ordinal = re.compile(r'(?i)((ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|one|two|three|four|five|six|seven|eight|nine|hundred|thousand|million|billion|trillion)[ -]*)*(whole|first|second|half|halves|third|fourth|quarter|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteetn|seventeenth|eighteenth|nineteenth|twentieth|thirtieth|fortieth|fiftieth|sixtieth|seventieth|eightieth|ninetieth|hundredth|thousanth|millionth|billionth|trillionth)(s)?')


    #Make sure we do not convert decimals, fractions, or ordinals
    #Find all possible matches of those in the text, then record their indices in list arr so we know which ranges of indices not to convert
    #Later, with each match found for re.finditer(RE_main,text) we will check if the indices of the given match
        #lie within a non conversion range by checking with the values in arr. If that is the case, we skip all conversion steps and move to the next match
    arr = [1] * len(text)
    for b in re.finditer(RE_decimal, text):
        for i in range (b.start(),b.end()):
            arr[i] = 0

    for c in re.finditer(RE_fractional_or_ordinal, text):
        for i in range (c.start(),c.end()):
            arr[i] = 0



    for m in re.finditer(RE_main, text):

        match_group = "{}".format(m.group())

        big_number = False
        total_value = 0

        convert = True
        for i1 in range (m.start(),m.end()):
            if arr[i1]==0:
                convert = False
                break


        if convert == True:

            #for big numbers!
            #this means numbers that include positional values: thousand, million, billion, and/or trillion
            #essentially we divide the word into groups based on the positional terms
                #within each group we check to see if there are
                    # ( (ones) and (hundred) )? and ( (teens) or ( (tens) and/or (ones) ) )  of course followed by (positional)
                #we convert each found group to a corresponding int number, then add them accordingly, then find the value of the positional and multiply them
                #repeat
            if re.search(RE_pos,m.group())!=None:
                big_number = True
                pos_lst = re.finditer(RE_pos, m.group())
                pos_index = [i.end() for i in pos_lst]
                pl = len(pos_index)
                pos_index.insert(0,0)
                pos_index.append(len(m.group()))
                str1 = "{}".format(m.group())

                total_value = 0

                for i in range (0,pl+1):

                     ones_hundred_digit = 0
                     teens_digit = 0
                     tens_digit = 0
                     ones_digit = 0
                     teens_included = False

                     sub = str1[pos_index[i]:pos_index[i+1]]
                     if sub=="" or re.fullmatch(RE_space, sub): break

                     match0 = re.search(RE_ones_hundred, sub)
                     if match0!=None:
                        match0_end = match0.end()
                        for j in range(2,11):
                            if match0.group(j)!=None:
                                ones_hundred_digit = (j-1)*100;
                                sub = sub[match0_end:]

                     match1 = re.search(RE_teens, sub)
                     if match1 != None:
                        for k in range(2, 12):
                            if match1.group(k) != None:
                                teens_digit = (k-2)+10;
                                teens_included = True

                     if teens_included == False:
                         match2 = re.search(RE_tens, sub)
                         if match2 != None:
                            match2_end = match2.end()
                            for l in range(2, 10):
                                if match2.group(l) != None:
                                    tens_digit = l*10;
                                    sub = sub[match2_end:]

                         match3 = re.search(RE_ones, sub)
                         if match3 != None:
                            for m in range(2, 11):
                                if match3.group(m) != None:
                                     ones_digit = m-1;

                     pos_value = 1
                     match4 = re.search(RE_pos, sub)
                     if match4 != None:
                        str2 = re.search(RE_pos_no_spaces, "{}".format(match4.group())).group()
                        if  re.fullmatch(r'(?i)thousand',str2):
                            pos_value = 1000
                        elif re.fullmatch(r'(?i)million',str2):
                            pos_value = 1000000
                        elif re.fullmatch(r'(?i)billion',str2):
                            pos_value = 1000000000
                        elif re.fullmatch(r'(?i)trillion',str2):
                            pos_value = 1000000000000

                     total_digits = ones_hundred_digit + teens_digit + tens_digit + ones_digit
                     if total_digits == 0: total_digits = 1
                     total_value = total_value + pos_value*total_digits



            #for small numbers!
            #We make the assumption that numbers like "twenty three hundred" = 2300 can only be small numbers (numbers that do NOT include positional terms like thousand, million, bllion, or trillion)!
            if big_number == False:
                str1 = "{}".format(m.group())
                while str1 != "":

                    ones_hundred_digit = 0
                    teens_digit = 0
                    tens_digit = 0
                    ones_digit = 0
                    teens_included = False
                    hundred_present = False
                    end = len(str1)

                    match4 = re.search(RE_hundred, str1)
                    if match4 != None:
                        end = match4.end()
                        hundred_present = True
                    match1 = re.search(RE_teens, str1[:end])
                    if match1 != None:
                        match1_end = match1.end()
                        for k in range(2, 12):
                            if match1.group(k) != None:
                                teens_digit = (k - 2) + 10;
                                teens_included = True
                                str1 = str1[match1_end:]
                                end = end - match1_end

                    if teens_included == False:
                        match2 = re.search(RE_tens, str1[:end])
                        if match2 != None:
                            match2_end = match2.end()
                            for l in range(2, 10):
                                if match2.group(l) != None:
                                    tens_digit = l * 10;
                                    str1 = str1[match2_end:]
                                    end = end - match2_end


                        match3 = re.search(RE_ones_forward, str1[:end])
                        if match3 != None:
                            match3_end = match3.end()
                            for m in range(2, 11):
                                if match3.group(m) != None:
                                    ones_digit = m - 1;
                                    str1 = str1[match3_end:]
                                    end = end - match3_end

                    total_digits =  teens_digit + tens_digit + ones_digit
                    if total_digits == 0: total_digits = 1

                    if hundred_present==True:
                        total_digits = total_digits * 100
                        str1 = str1[end:]

                    total_value = total_value + total_digits


            #now replace the word-cardinal-numbers with the corresponding digits = total_value
            #replace the match number group with the string conversion of total_value making sure to keep correct spaces before and after
            index_last_word_char = len(match_group)
            if re.search(RE_word_char_before_following_space, match_group) != None:
                index_last_word_char = re.search(RE_word_char_before_following_space, match_group).start()+1
            text = text.replace(match_group[:index_last_word_char], str(total_value),1)


    #final part!
    #handle situations like "a hundred", "a thousand", "a million", "a billion", "a trillion". We consider these numbers positional/pos numbers
    #We will not handle situations where it is "a" + a non pos number, ex. "a ten hundred" = "a 10000", "a-seventeen" = "a-17", "a two trillion" = "a 2000000000000", etc
    #We include numbers like "-a hundred seventy one-" = "-171-" where there is "a" followed directly by a pos number, the values after that are irrelevant
    #Since we have already converted all cardinal numbers in the text, we now find the digit numbers and check if they within the correct ranges to be meet the above qualifications
        #Then we remove the corresponding "a" in the text
    RE_final_part = re.compile(r'(?i)a[ -]+1\d*')
    RE_numeral = re.compile(r'\d+')
    while re.search(RE_final_part, text) != None:
        z = re.search(RE_final_part, text)
        z_start = z.start()
        number = re.search(RE_numeral, z.group())
        number_str = "{}".format(number.group())
        x = int(number_str)
        if (100<=x and x<200) or (1000<=x and x<2000) or (100000<=x and x<200000) or (1000000<=x and x<2000000) or (100000000<=x and x<200000000) or (1000000000<=x and x<2000000000) or (100000000000<=x and x<200000000000) or (1000000000000<=x and 2000000000000):
            text = text[:z.start()] + text[number.start()+z.start():]

    return text



def normalize_extra(text):
    # TODO: to be updated
    return text


if __name__ == '__main__':
    S = [
        'I met twelve people',
        'I have one brother and two sisters',
        'A year has three hundred sixty five days',
        'I made a million dollars',
        'Thirteen January: Today I walked by and saw seventy six to maybe a hundred ten soldiers passing by me, it was kind of worrisome, but still alot less than what must have yesterday been Twenty Three Hundred! TWENTY THREE HUNDRED!!! Whatever, there were twenty-one of us, twenty-two point half if you included my' \
        ' nine-year-old brother. I think that even with just our main range of twelve to    ---fifteen--- of us we could take on nineteen billion eighty six million nine hundred thousand two hundred-twenty one if we had to! Or at least I tried to calm myself thinking so...Anyway, other than' \
        ' that we went to the store on Fifth Avenue - or is it sixth?- and got some pizzes for thirty seven point ten dollars, they had to split the a hundred dollars I had into smaller bills. Six dozen boxes is how much we got. We split the boxes into fifths or each of us. I had two thirds of' \
        ' a box by myself.'
    ]

    T = [
        'I met 12 people',
        'I have 1 brother and 2 sisters',
        'A year has 365 days',
        'I made 1000000 dollars',
        '13 January: Today I walked by and saw 76 to maybe 110 soldiers passing by me, it was kind of worrisome, but still alot less than what must have yesterday been 2300! 2300!!! Whatever, there were 21 of us, twenty-two point half if you included my 9-year-old brother. I think that even with just our main range of 12 to    ---15--- of us we could take on 19086900221 if we had to! Or at least I tried to calm myself thinking so...Anyway, other than that we went to the store on Fifth Avenue - or is it sixth?- and got some pizzes for thirty seven point ten dollars, they had to split the 100 dollars I had into smaller bills. 6 dozen boxes is how much we got. We split the boxes into fifths or each of us. I had two thirds of a box by myself.'
    ]

    correct = 0
    for s, t in zip(S, T):
        if normalize(s) == t:
            correct += 1

    print('Score: {}/{}'.format(correct, len(S)))