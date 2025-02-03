#### Prompt Creation Process

#### Basic information for getting lab started 
1. Merge repository with "git fetch profremote' and 'git merge profremote/main'
2. install ollama with 'pip install ollama'
3. add ollama using 'ollama pull lamma3.2:latest'

#### Capabilities of the DnD Dungeon Master
1. Generate a random story
2. Take the players on an adventure in the fantasy world of DnD.
2. Create NPC characters
3. Manage the game world
4. Make changes to player character sheets
5. Implement a turn-based combat system
6. Help the user through character creation

>Note: This agent is meant to imitate a dungeon master, however the prompts created for the agent 
are heavily focused around perfecting character creation.

#### First approach 
#### Intention
>Get the system to act like a dungeon master for the game Dungeins and Dragons.

#### Action/Change
>Added a message with system role which tells the system that is it a dungeons and dragons master. Did not add any options. 

#### Result
>When I gave it a random DnD 'scene' or 'play' that I found online, it expanded on the scene and provided a good description.
However, the response time was very slow and the description was a bit too long.

#### Reflection/Analysis of Result
>By telling the system that it was a Dungeon Master, it knew how it should respond. Because I provided no options,
there was not limit for the amount of tokens the agent outputs which could account for response length. As far as response
time, I'm not sure that there is a way to improve it.

#### Second approach
#### Intent
>I want the system to be more random and limit the response length.
Finally, I want the user to be able to gracefully end the game play by typing '/exit'.

#### Action/Change
>Added a temperature of 0.5 in hopes that it will guide the story in a more random/unexpected way.
Also added a max_token of 100 to make the reponse more concise.
In the chat loop, added the user role message after the assitant role message so that the last message in the messsages list is from the user--allows user to exit the chat by entering '/exit'. 

#### Results
>User is now able to exit chat and atttempts.txt file created. DM is engaging with user by asing questions such as 'What do you do next?Not giving user enough options, making the narritave too broad.

#### Reflection/Analysis of Results
>The response is much shorter because I added the max_tokens option. The agent could not be engaging with the user 
because I didn't explicity tell it to. 

#### Third approach 
#### Intention
>I want the agent to engage more with the user by asking them questions or perhaps providing them with options.

#### Action/Change
>Added another message with system role a gave the context: 'You should provide a fun and engaging experience.'

#### Result
Engages with the user more by providing description and giving the user options on what to do next. Has the exact same format everytime--provides description and give the user four options. This could become monotonous.

#### Reflection/Analysis of result
It seems that adding another message for the system pushed the model to be a more effective/engaging DM.


#### Fourth attempt
#### Intention
>I want to make the agent more interactive when the user is creating a character. The agent seems to have an 
accurate list of DnD classes, but I want the user to have the ability to determine their race, abilities, 
skills, tools and background as well.

#### Action/Change
>I will add a system prompt that tells the agent to allow the user to create a character by choosing race, 
class, and use the rolling dice method to determine their skills. I will tell the agent that I want
skills to be determined based on rolling dice. Then I want the agent to automatically determine
the characters skills, tools, and background. 
>I think this will help the agent better understand what steps it should take for character creation.

#### Result
>After adding the additional prompt, the agent correctly went throught the steps of creating a character 
when I told it I wanted to play dungeons and dragons.

#### Reflection/Analysis of the result. 
>I think it worked because I explicity told the agent what it should do through a detailed prompt--more 
specifically I tried to create a superprompt. 
>This worked for the most part, as described above. As a specific example, I told the agent I
wanted it to 'Guide the user through the rolling process and record the scores', and it did exactly that, 
rather then generate the abilities "behind the scenes" so to speak.
>The only issue I found is that the agent is telling the user to name their character after they choose a class
but not actually allowing them to do so.

#### Fifth attempt 
#### Intention
>I want to fix the agents issue in not allowing the user to create a name for their character after selecting
a class.

#### Action/Change
>I am going to add to the previous prompt that I want the system to prompt the user to enter a name for their
character after selecting their class.

#### Result
>I believe that the agent actually became worse at character creation. For example, it now provided
the user with options to select tools, but never allowed them to select any. Meanwhile, I do not want the 
agaent to provide any options for tool, skills, or background at all, but rather generate these aspects of 
the character automatically.

#### Reflection/Analysis of Result
>The only reason I can think of for the agents changed behavior is due to rewording in the prompt. Specifiaclly, 
adding the part: "Afterwards, you will allow the user to create a name for their character, then move on to the
next step. The user will be able to choose their class based on a class list you provide." It seems that the system
is not registering the part when I tell it to prompt for a character name at all.

#### Sixth attempt
#### Intention
>I want to:
1. Make the agent prompt the user for a character name
2. Make the system automatically select the characters tools, skills, and background

#### Action/Change 
>I am going to re-word the section in the prompt where I tell the system to ask the user to make a character 
name. I am also going to give the agent an example of what a reply should look like when creating a characters tools
based on past successful attempts.

#### Result 
>I believe that this action made the system's performance decrease. I tried to give the agent an example of how to output the character's background, specifically I wanted the agent to generate the background automatically rather than giving the user options.
Although the agent did generate the characters background automatically, it did so before the user created the character. The agent
also did not ask the user to inout a name for the character.

#### Reflection/Analysis of Result
>I think the reason why the agent started talking about background story first is because I added the prompt as an assistant
role at the end of the messages dictionary. This could have made the agent believe that it should be the first thing it outputs/talks
about. I tried to follow the textbook's example of one-shot learning to help the system follow a certain format in it's response,
however upon rereferncing the textbook, I possibly should have provided an example user prompt as well, and formatted the assistant prompt better.

#### Sixth attempt
#### Intent
>I want to make the agent have a clear flow of character creation process, because as of now it seems to be confused 
on what steps to follow in order/how to go about handling getting information about a specific feature of a character 
(whether to give the user options, prompt them for info, or create it automatically).

#### Action/Change
>I'm going to break the prompt down into steps for the system, and be more clear on how I want the agent to engage with the user.
For example, I'm going to tell the system what it should say to the user when it's time to get the characters name (e.g 'What
is your characters name?').

#### Result 
>This worked very well in tailoring the agent to what I wanted it to do. This time, the agent asked the user for the 
characters name and waited for their input. However, the agent still isn't performing exactly how i want it to when it comes
to gathering the character's abilities, skills, tools, and background. 

#### Reflection/Analysis of Result
>I think this worked because I was MUCH more detailed and specific in the prompt of what I wanted the system to do and 
I included certain phrases in the prompt that I want the agent to ask the user. I think that the more specific and detailed I 
make the prompt, the better the agent performs.

#### Seventh attempt
#### Intention
>My agent is working well, but the last thing I want to do is to fix a few details about gathering the characters
abilities, skills, tools, and background story. 

#### Action/Change
1. I want to tell the system that it should guide the user through each step in the process of determining their 
characters abilities. 
2. I am going to expand on the sentence where I tell the user to automatically choose skills, tools, and background and
possibly break it down into seperate sentences so the system knows that these are seperate steps.

#### Result
>The agent did what I wanted it to do. It prompted the user to input a name, it went through the process of rolling dice
to select the character's abilities, and it autonatically came up with the characters skills, tools, and background story. Additionally,
it did so in the correct order.

#### Reflection/Analysis of Result
>The agent went through the process of rolling dice with the user because I explicity told to go through the process
'step-by-step'. Then, I broke down the gathering of skills, tools, and background into three different sentences in the prompt
so the system could know how to better deal with each aspect. I also told the agent specifically that it shpuld generate a 
**unique** backstory once it has gathered all other information (e.g. race, class, abilities...)









