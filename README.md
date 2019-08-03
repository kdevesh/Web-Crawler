This program is a web crawler which crawls the seed url specified in configuration/config.yml for all the urls on that web page.
After crawling it saves the urls in the repository.txt file and then starts crawling again from the repository.txt
The program gets stopped when the user hits Ctrl+C or when the number of urls to parsed becomes equal to numberOfLinks specified in config.yml
The logs are created based on timestamp and the logs gets logged in the file for future reference as well as on the terminal for the user to see.
