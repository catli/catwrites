Title: Scraping School and District Data
Slug: how_to_scrape_school_data 
Tags: NCES, scrape, data, schools
Date: 2015-7-01

When looking at trends for school and district level data, there are many local factors that could influence outcomes. For example, variables such as a school's size or social-economic makeup could be predictors of success. Much of this data is publicly available on the National Center for Education Statistics (NCES) [website](https://nces.ed.gov/), but in a difficult to extract format. In order to get the data for a large number of schools, we have to use scrapping methods . Below is an example of application using BeautifulSoup. This retrieves data for all schools in districts using a csv file listing nces id for each district but can be manipulated to feed in district name parameter instead.

Here are some libraries you will need to import

    :::python
    from bs4 import BeautifulSoup as bs
    import requests 
    import csv
    # be polite to nces and sleep between pages
    from time import sleep 

As well as some helpful functions for scrapping the data 

    :::python
    def fetch_district(district_id):
        #fetches the search links and names of districts from which we can retrieve school level data
        response = requests.get('http://nces.ed.gov/ccd/districtsearch/district_detail.asp?ID2=%s' % district_id)
        soup = bs(response.text)
        tag = soup.find(text='District Name:').parent.parent.parent
        font = [c for c in list(tag.findAll("font"))]
        districts = str(font[1].text)
        sublinks = str(font[2].a["href"]) #need to edit so that it calls the link rather than the tedxt
        links='http://nces.ed.gov/ccd'+sublinks.replace("..","")
        return districts, links

    def find_school(district,link):
        #argument: pass through the district search link
        #retrieves the school links and names for all the schools in district
        response = requests.get(link)
        soup = bs(response.text)
        tag = soup.find(text='School Name').parent.parent.parent.parent.parent.parent.parent.parent
        a = [c for c in list(tag.findAll("a"))]
        full_links = ['http://nces.ed.gov/ccd/schoolsearch/'+c["href"] for c in a]
        links = [c["href"] for c in a]
        names= [c.text for c in a]
        nexttrue = names[-1]=="Next >>"
        # if last element of link is a next page, recursive function call
        if nexttrue:
            nextlink='http://nces.ed.gov/ccd/schoolsearch/'+links[-1]
            del full_links[-1]
            del names[-1]
            nextschools=find_school(district,nextlink)
            full_links=full_links+nextschools[0]
            names=names+nextschools[1]
        #return links and names
        del full_links[-1]
        del names[-1]
        return full_links, names

    def fetch_school(school_id):
        response = requests.get('http://nces.ed.gov/ccd/schoolsearch/school_detail.asp?ID=%s' % school_id)
        soup = bs(response.text)
        tag = soup.find(text='Total Students:').parent.parent.parent.parent
        td = [c for c in list(tag.children) if c.name == 'td']
        students = td[-1].text
        tag = soup.find(text='Free lunch eligible: ').parent.parent.parent
        td = list(tag.children)
        free = td[-1]
        tag = soup.find(text='Reduced-price lunch eligible: ').parent.parent.parent
        td = list(tag.children)
        reduced = td[-1]
        tag = soup.find(text='Title I School:').parent.parent.parent
        td = list(tag.children)
        title1 = td[-1].find("Yes")==1         
        tag = soup.find(text='Mailing Address:').parent.parent.parent
        address = tag.find("br").text
        return students, free, reduced, title1, address

    def extract_school_nces(list):
        #function to extract school nces from a string
        code_list = []
        for item in list:
            index = item.find("&ID")+4
            code = item[index:index+13]  #nces code has 13 numbers
            code_list.append(code)
        return code_list

And other functions to open and write flat files:

    :::python
    def csv_open(file):
        #opens a csv file with one column 
        #Argument: file = a string with the csv file name 
        #Output: an array with the csv file
        with open(file, 'rU') as csvfile:
            csvobject = csv.reader(csvfile, delimiter=',', quotechar='|')
            array = [row for row in csvobject]
        return array

    # Write csv file. 
    # If necessary first - zip together list 
    # Then push row to object and write the rows 
    # If in list form, use write_csv , otherwise  use csv_export
    def csv_export(file,rows):
        # export rows as file
        with open(file, 'wb') as f:
            writer = csv.writer(f)
            writerows(writer,rows)

    def writerows(self, rows):
        # push rows into object 
        for row in rows:
            self.writerow(row)

    def ziparray(*lists):
        #zip together lists for export
        ziplist = [ list(x) for x in zip(*lists) ]
        return ziplist

    def write_csv(file,*lists):
        #call previous functions to write csv
        rows = ziparray(*lists)
        csv_export(file,rows)

Given a set of nces id for districts, the below script fetches data relevant data for each school.


    :::python
    district_nces = csv_open("sample_nces.csv")

    dist_mat =[]

    for d in district_nces:
        district=d[0]
        try: #try to fetch district
            d_array = fetch_district(district)
        except AttributeError: #if the code does not work
            pass
        d_name = d_array[0]
        d_link = d_array[1]
        # find the array of schools assocated with that district
        sch_array = find_school(d_name,d_link)
        sch_links = sch_array[0]
        sch_name = sch_array[1]
        sch_nces = extract_school_nces(sch_links)
        sch_mat = ziparray(sch_nces,sch_links,sch_name)
        #push district data to each row
        for row in sch_mat:
            row.append(d_name)
            row.append(d_link)
            row.append(district)
        #push school data to amtrix 
        for row in sch_mat:
            s = row[0]
            try:
                sch = fetch_school(s)
            except AttributeError:
                pass
            for item in sch:
                row.append(item)
            #push data to district matrix
            dist_mat.append(row)
        #append the district data to matrix 
        sleep(1)

    #convert unicode to ascii which can be exported 
    rowindex=0
    for row in dist_mat:
        colindex=0
        for c in row:
            if isinstance(c,unicode):
                row[colindex] = c.encode('ascii','ignore')
            colindex+=1
        rowindex+=1

    csv_export("district_nces_scrape_output.csv",dist_mat)
