import discord
from discord.ext import commands
from discord import Intents
import time
import random
import community 
import seinfeld

client = commands.Bot(command_prefix="?", intents=Intents.default(), help_command=None)


players = {}

@client.event
async def on_ready():
  print("")
  print("The bot is ready.")
  await client.change_presence(activity=discord.Game(name="Sitcom Triva Game!"))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('?hello'):
    await message.channel.send('Hello!')
  else:
    await client.process_commands(message)

@client.command()
async def test(ctx):
  await ctx.send("La victoria es para R.O.B.")

#Command to start the game. 
@client.command()
async def startGame(ctx):
  #Telling users a new game is starting. 
  prompt = discord.Embed(title = "New Game Start!")
  prompt.add_field(name="Points refresed! It's time to start a new game!", value="")
  await ctx.send(embed=prompt)

  chooseCat = discord.Embed(title="What category do you want?")
  chooseCat.add_field(name="Options: ", value="- Community\n- Seinfeld\n- Quit")
  await ctx.send(embed=chooseCat)

  gameCat = discord.Embed(title="The category is...") #Embed item for confirming the selected game category. 
  chosenCategory = False #Boolean variable checking if a category has been chosen yet. 
  stopGame = False #Stops the game. 
  questionNumber = 0 #Number of questions wanted for the game.

  choice = "default" #Variable for the category chosen.

  #while-loop. Waits for user to choose a category. 
  while (chosenCategory == False):
    response = await client.wait_for("message")
    
    
    chosenCategory = True #Temporary setting variable to true if a valid category is chosen. 

    #If-else statement. Sets embedded object based on the category chosen.     
    if (response.content.lower() == "community"):
      gameCat.add_field(name="Community", value="")
      choice = "community"
    elif (response.content.lower() == "seinfeld"):
      gameCat.add_field(name="Seinfeld", value="")
      choice = "seinfeld"
    elif (response.content.lower() == "quit"):
      stopGame = True
      choice = "quit"
    else:
      chosenCategory = False
      
      tryAgain = discord.Embed(title="Please input a valid category...")
      tryAgain.add_field(name="Options: ", value="- Community\n- Seinfeld\n- Quit")
      await ctx.send(embed=tryAgain)

  #If-else statement. Proceeds with the game unless the user chose to quit. 
  if (stopGame == False):
    chooseNum = discord.Embed(title="How many questions would you like to play?")
    chooseNum.add_field(name="Options: ", value="- Enter value between 5 and 20\n- Quit")

    await ctx.send(embed=chooseNum)

    validNumber = False #Boolean value to ensure a valid number of questions were chosen. 

    #while-loop. Loops through options while waitig for user to input a valid number of questions. 
    while (validNumber == False):
      validNumber = True #Temporarily sets validNumber to true in anticipation of a true value being entered. 

      response = await client.wait_for("message")
      

      #if-statement. Checks if valid number was input. 
      if (response.content.lower() == "quit"):
        stopGame = True
        await ctx.send("Oh, so you don't want to play? :frowning:")
      elif (response.content.isdigit() == False):
        validNumber = False

        tryAgainNum = discord.Embed(title="Please enter a valid number...")
        tryAgainNum.add_field(name="Options: ", value="- Enter value between 5 and 20\n- Quit")

        await ctx.send(embed=tryAgainNum)
      else:
        #if-else statement. If the response is a proper digit, we need to further assess it. Otherwise, the game begins. 
        if (int(response.content) < 5 or int(response.content) > 20):
          print(response.content)
          validNumber = False

          tryAgainNum = discord.Embed(title="Please enter a valid number...")
          tryAgainNum.add_field(name="Options: ", value="- Enter value between 5 and 20\n- Quit")

          await ctx.send(embed=tryAgainNum)
        else: 
          questionNumber = int(response.content)

          beginGame = discord.Embed(title="The game begins now!")
          await ctx.send(embed=beginGame)

          time.sleep(0.25)
          remember = discord.Embed(title="REMEMBER: YOU ANSWER BY ONLY TYPING THE NUMBER (E.G. 1)")
          await ctx.send(embed=remember)

          time.sleep(1.0)

          chosenQuestions = {} #Dictionary to keep track of which questions have been chosen and are in play. 

          questions = [] #List of questions currently being used in the game.
          correct = [] #List of correct answers in the game. 
          options = [] #List of options that correspond to each question.

          score = {} #Dictonary to keep track of score. 

          isCorrect = False #Boolean variable determining if answer is correct or not. 

          #If-else statement. If the user chooses a mixed category, the bot will specfically prepared mixed questions.
          #Otherwise, it will choose questions from one category as normal. 
          if (choice == "mixed"):
            #Note: Mixed Feature was scrapped due to time issues. 
            await ctx.send("Let's-a-go!")
          else:
            await ctx.send("Let's-a-go!")
            
            

            #For-loop. Generates the number of questions that the user wanted, ensuring each is unique.
             
            for x in range(questionNumber):
              generatedQuestion = random.randrange(20)
              

              isInThere = False #Boolean value seeing if a question is already in the dict. 
              print(generatedQuestion)

              #While-loop. Generates random index value until it's one not in the dictionary and thus not already chosen.
              while (isInThere == False):
                generatedQuestion = random.randrange(20)
                print(generatedQuestion)

                #if-statement. If the question is not in the dict, isInThere is false and while loop is broken to add it.
                if (generatedQuestion in chosenQuestions):
                  isInThere = True
                else:
                  chosenQuestions.update({generatedQuestion : x})
              

            #IF-else statement. Will pull questions from the appropiate category. 
            if (choice == "community"):
              for key in chosenQuestions:
                questions.append(community.questions[key])
                correct.append(community.correct[key])
                options.append(community.options[key])
            elif (choice == "seinfeld"):
                for key in chosenQuestions:
                  questions.append(seinfeld.questions[key])
                  correct.append(seinfeld.correct[key])
                  options.append(seinfeld.options[key])

          #Running through each question. 
          for x in range(questionNumber):
            isCorrect = False

            currQuestion = discord.Embed(title="Question #" + str(x + 1) +"\n" + questions[x])

            #Getting all the choices for each question.
            for y in range(len(options[x])):
              currQuestion.add_field(name=str(y + 1) + ". " + options[x][y], value="\n")
            
            await ctx.send(embed=currQuestion)

            #While-loop. Bot will not proceed until a correct answer is inputted. 
            while (isCorrect == False):
              answerText = await client.wait_for("message") #Gets answer in text form. 
              print(answerText)
              
              #If-statement. If the answer the user provides is an integer value, check for correctness. 
              if (answerText.content.isdigit() == True):
                answerNum = int(answerText.content)
                checkAnswer = options[x][answerNum - 1]

                #If-else statement. Checks if answer is correct. 
                if (checkAnswer == correct[x]):
                  await ctx.send("That is correct!")
                  isCorrect = True
                  time.sleep(0.5)

                  #If-else statement. Checks if user is already in the score keeper or not and adds a point. 
                  if (answerText.author in score):
                    score.update({answerText.author : score.get(answerText.author) + 1})
                    await ctx.send(answerText.author.mention + " now has " + str(score.get(answerText.author)) + " points")
                  else:
                    score.update({answerText.author: 1})
                    await ctx.send(answerText.author.mention + " now has 1 point")

                  time.sleep(0.5)

                  #If all questions are answered, end game. Else move to next question.
                  if (x == questionNumber - 1):
                    await ctx.send("Game Set!")

                    winScore = 0
                    winUser = answerText.author
                    winners = [] 

                    #For-loop. Goes through all the users in the score to find winners.
                    for key in score:
                      #If else statement. If a new highest score is found, the list of winners is erased and there is now a new winner.
                      #If an equal score is found, user is added to list of winners. 
                      if (score.get(key) > winScore):
                        winners = [key]
                      elif (score.get(key) == winScore):
                        winners.append(key)

                    #For loop. 
                    time.sleep(0.25)
                    
                    #If-statement. Special win messages are printed depending on the number of victors.
                    if (len(winners) == 1):
                      await ctx.send(winners[0].mention + " wins!")
                    elif (len(winners) == 0):
                      await ctx.send("Nobody won. :frowning:")
                    else:
                      for i in winners:
                        await ctx.send(i.mention)
                      await ctx.send(" ... all win!")
                    
                  else:
                    await ctx.send("Time for the next question!")
                  


              

              


  else:
    await ctx.send("Oh, so you don't want to play? :frowning:")


#Token can be swapped out for actual token.
client.run('TOKEN')