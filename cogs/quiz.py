import asyncio
import json
import random
from data.question import Question
from discord.ext import commands


class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.questions = self.get_questions()
        self.option_emojis = ["🇦", "🇧", "🇨", "🇩"]
        self.scores = {}  # Dictionary to store user scores
    

    def get_questions(self):
        with open("data/questions.json", "r") as f:
            questions = json.load(f)
        
        questions_list = []
        for question in questions:
            question_obj = Question(question["Question"], question["Options"], question["CorrectAnswer"])
            questions_list.append(question_obj)
        return questions_list


    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready!')

    @commands.command()
    async def playquiz(self, ctx):
        question = random.choice(self.questions)
        print(question.options)
        question_message = await ctx.send(f"**Quiz Question:**\n{question.question}\n\nOptions:\n" +
                                          "\n".join(f"{key}. {value}" for key, value in question.options.items()))

        for emoji in self.option_emojis:
            await question_message.add_reaction(emoji)
        
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["🇦", "🇧", "🇨", "🇩"]
        
        def emoji_flag_to_country_code(emoji_flag):
            # Offset between uppercase ASCII letters and regional indicator symbols
            offset = ord('🇦') - ord('A')
            # Extract the country code letter
            country_code_letter = chr(ord(emoji_flag) - offset)
            return country_code_letter

        try:
            reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=30.0)
            selected_option = emoji_flag_to_country_code(str(reaction.emoji))
            if not question.is_answered and question.options[selected_option] == question.options[question.correct_answer] and user.id not in question.answers:
                await ctx.send(f"Correct! {ctx.author.mention} gets a point.")
                question.answers[user.id] = selected_option
                question.is_answered = True
                self.scores[ctx.author.id] = self.scores.get(ctx.author.id, 0) + 1
            elif user.id in question.answers:
                await ctx.send("You have already answered this question.")
            elif self.is_answered:
                await ctx.send("This question has been answered already.")
            else:
                await ctx.send(f"Incorrect.")
                question.answers[user.id] = selected_option
        except asyncio.TimeoutError:
            await ctx.send("Quiz Timed Out!")
    
    @commands.command()
    async def scores(self, ctx):
        score_message = "\n".join(f"{ctx.guild.get_member(user_id).display_name}: {score}"
                                  for user_id, score in self.scores.items())
        await ctx.send(f"Quiz Scores:\n{score_message}")


async def setup(bot):
    await bot.add_cog(Quiz(bot))