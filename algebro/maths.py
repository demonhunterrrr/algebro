from lib2to3.pgen2.tokenize import TokenError
from multiprocessing.resource_sharer import stop
from sympy import Symbol, solve, Eq, preview, parse_expr
import discord
from discord.ext import commands
from discord.ui import Button, View
from sympy.parsing.sympy_parser import standard_transformations,implicit_multiplication_application
transformations = (standard_transformations +(implicit_multiplication_application,))
from random import *
import re
import asyncio
from tokenize import TokenError

class GiveUpButton(discord.ui.View):
  @discord.ui.button(label="Give Up", style=discord.ButtonStyle.red, emoji="😭")
  async def button_callback(self, button, interaction, pressed):
      button.disabled = True # set button.disabled to True to disable the button
      await interaction.response.edit_message(view=self) # edit the message's view
      pressed += 1

class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pressed = 0
    
    async def user_part(self, x, solution, ctx):
        def check(msg):
            return msg.author.id != self.bot.user.id and msg.content.lower()[0] == "x" and self.pressed == 0
        try:
            msg = await self.bot.wait_for('message',timeout=300.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Nobody has answered for five minutes, so the question has been cancelled.")
            return

        for i in solution:
            try:
                if parse_expr(re.sub('[Xx=]','',msg.content), transformations=transformations) == i : await ctx.send(f"Good job <@{msg.author.id}>! You got it correct!"); return
            except TokenError:
                await ctx.send(f"Sorry, but I can't compute that."); await self.user_part(x, solution, ctx); return
        preview(Eq(x,solution[0]),output="png", viewer="file", filename="solution.png", fontsize=36, euler=False, dvioptions=['-D','1600',"-bg", "Transparent","-fg", "White", "-T", ""])
        
        give_up = Button(label="Give up",style=discord.ButtonStyle.red, emoji="😭")
        view = View()
        view.add_item(give_up)
        async def give_up_button(interaction):
            try:
                if self.pressed != 0: await interaction.response.defer()
                await interaction.response.send_message("Well, you failed. The answer was", file=discord.File("solution.png"))
                self.pressed += 1
            except:
                pass
                
        give_up.callback = give_up_button
        await ctx.send(f"Sorry <@{msg.author.id}>, but your mom doesn't love you anymore! (You're wrong)",view=view)
        await self.user_part(x, solution, ctx)

    @commands.command(name="literal_equation",help="Sends a literal equation for the user to solve. Answer must start with \"x =\"!!!")
    async def literal_equation(self, ctx):
        x = Symbol("x")
        y = Symbol("y")
        ops = ["+","-","/"]
        left_side = parse_expr(f'{choice(["+","-"])}{randint(1,10)} * {x} {choice(ops)}{randint(1,100)}',evaluate=False)
        right_side = parse_expr(f'{choice(["+","-"])}{randint(1,10)} * {y} {choice(ops)}{randint(1,100)}', evaluate=False)
        equation = Eq(left_side,right_side)
        preview(equation,output="png", viewer="file", filename="equation.png", fontsize=36, euler=False, dvioptions=['-D','1600',"-bg", "Transparent","-fg", "White"])
        await ctx.send(f"Solve for x",file=discord.File("equation.png"))
        await self.user_part(x, solve(equation,x), ctx)
    
    @commands.command(name="linear_equation", help="Sends a linear equation for the user to solve. Answer must star with \"x = \"!!!")
    async def linear_equation(self, ctx):
        x = Symbol("x")
        ops = ["+","-"]
        left_side = parse_expr(f'{choice(ops)}{randint(1,10)}({choice(ops)}{randint(1,10)}*{x} {choice(ops)} {randint(1,10)} )', evaluate=False, transformations=transformations)
        right_side = parse_expr(f'{choice(ops)}{randint(1,10)}({choice(ops)}{randint(1,10)}*{x} {choice(ops)} {randint(1,10)} ) {choice(ops)}{randint(1,25)}', evaluate=False, transformations=transformations)
        equation = Eq(left_side,right_side)
        preview(equation,output="png", viewer="file", filename="equation.png", fontsize=48, euler=False, dvioptions=['-D','2000',"-bg", "Transparent","-fg", "White"])
        await ctx.send(f"Solve for x",file=discord.File("equation.png"))
        await self.user_part(x, solve(equation,x), ctx)
