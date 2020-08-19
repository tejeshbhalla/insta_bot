
import selenium
from selenium import webdriver
from time import sleep 
import random
import warnings

path='C:\Program Files (x86)\chromedriver.exe' 


class Insta_bot():

	def __init__(self,path):
		self.path=path
		self.url='https://www.instagram.com/'
		self.driver=webdriver.Chrome(path)
		self.comments=['Amazing Post','Loved it !','Damn that was lit!'] #list storing the random comments we will use 
		self.home_page=False # boolean expression to tell us that we are not logged in 
	def init_connection(self,username,password): #method to intialize the login and navigate us to the home page 
		self.username=username 
		self.driver.get(self.url)
		sleep(3) #time library method to instantiate a pause method 
		username_input=self.driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input')
		username_input.send_keys(username)
		password_input=self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
		password_input.send_keys(password)

		sign_in_btn=self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button')
		sign_in_btn.click()

		sleep(5)

		not_now_btn=self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button')
		not_now_btn.click()
		sleep(5)
		#not now box
		not_now_box_btn=self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]')
		not_now_box_btn.click()

		#make a variable that verifies that we are logged in and on the home page 
		self.home_page=True


	def verify_logged_in(self):
		print(self.home_page)
		if self.home_page==True:
			return True
		else:
			warnings.warn('Press 1 to log in first')
			return False


	def like_random_hastags(self,hashtag):
		if self.verify_logged_in():
			sleep(1)
			#this method will search for a random hastag and start liking and commenting on random posts 
			input_search=self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input').send_keys('#'+str(hashtag))
			sleep(2)

			link_hashtag=self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[3]/div[2]/div/a[1]').click()

			sleep(3)

			all_posts_urls=self.driver.find_elements_by_tag_name('a')
			# this will give us all the links for the 'a' tag but we need to filter them as there could be links which are not for posts
			sleep(3)

			def filter_links(urls):
				return '.com/p/' in urls.get_attribute('href') # string check 


			all_posts_urls=list(filter(filter_links,all_posts_urls)) #filtering applied to all of the posts and then converted the elements back to a list from a generator object

			all_posts_urls=[i.get_attribute('href') for i in all_posts_urls]

			print(f'There are {len(all_posts_urls)} posts on the page how many of them would you like to spam ?')

			n=int(input('Enter the amount of posts you want to like and comment on :'))



			#now we will navigate to each post , and then like and comment on each  post 

			for i in all_posts_urls[:n]:
				self.navigate_to_link(i)
				sleep(2)
				self.like_and_comment(i)

			sleep(2)
			self.driver.get(self.url)

			return True

		else:
			print('You are not logged in ! press 1 and login first')
			err_response=True

			return err_response

	def navigate_to_link(self,link):
		sleep(3)
		self.driver.get(link)
		sleep(1)


	def like_and_comment(self,link):
		sleep(2)
		like_btn=self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button')
		like_btn.click()
		sleep(1)
		comment=random.choice(self.comments)
		# comment button
		div=self.driver.find_element_by_class_name('RxpZH').click()
		sleep(2)		
		#instagram expects user to click the div section first to activate the comment section
		sleep(3)
		comment_input_area=self.driver.find_element_by_xpath("//textarea[@placeholder='Add a comment…']").send_keys(comment+str(f'follow @{self.username} , for more such content'))
		sleep(3)
		post_btn=self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[3]/div/form/button').click()

		print('Liked And Commented On a Post')

	def follow_user(self,username):
		if self.verify_logged_in():
			self.nav_user(username)
		
			try :
				follow_button=self.driver.find_element_by_xpath("//button[contains(text(),'Follow')]")
				follow_button.click()
				sleep(1)
				print(f'followed {username} successfully')
				self.driver.back()

			except Exception as e:
				print(str(e),'Error')
			return False
		else:
			print('Log in First')
			return True


	def unfollow_user(self,username):
		if self.verify_logged_in():
			self.nav_user(username)
			follow_button=self.driver.find_elements_by_xpath("//button[contains(text(),'Follow')]")
			if follow_button:
				print('encounterd an error , either the element was not found or you are not following the user')
				sleep(2)
				self.driver.back()
			else:
				sleep(1)
				unfollow_btn=self.driver.find_element_by_class_name('_5f5mN.-fzfL._6VtSN.yZn4P')
				unfollow_btn.click()
				sleep(2)
				unfollow=self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[1]').click()
				sleep(3)
				self.driver.back()
			return False
		else:
			print('Log in First')
			return True




	def nav_user(self,username):
		if self.verify_logged_in():
			self.driver.get((self.url)+username)
			sleep(2)

		else:
			print('Log in First')
			self.init_connection()





if __name__=='__main__':
	path="C:\Program Files (x86)\chromedriver.exe"
	bot=Insta_bot(path=path)
	while True:
		print(""" Enter 1.To Initalize the connection and log in
Enter 2.To Start Hashtag Like and Bot spam
Enter 3.To Follow a User
Enter 4.To Unfollow as User 
Enter -1.To Exit """)

		action=int(input('Enter a valid choice : '))

		if action==1:
			username=input('Enter your username :')
			password=input('Enter your password :')
			bot.init_connection(username,password)
			continue 
		if action==2:
			hashtag=str(input('Enter the string for the hashtag :'))
			err=bot.like_random_hastags(hashtag)
			if err:
				continue
			else:
				continue



		if action==3:
			username=str(input('Enter the username of the user you want to follow :'))
			err=bot.follow_user(username)
			if err:
				continue
			else:
				continue

		if action==4:
			username=str(input('Enter the username of the user you want to unfollow :'))
			err=bot.unfollow_user(username)
			if err:
				continue
			else:
				continue



		else:
			exit()

