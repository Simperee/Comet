import discord
from discord.ext import commands
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash import cog_ext
import diseaseapi
import asyncio

guild_ids=[906560310217945150,844302791622131732,908835201562574858,895809572294496286,895083927591596042]

def generate_base_embed(embed, data):

    embed.add_field(name="Total cases", value = diseaseapi.format_number(data.cases))
    embed.add_field(name="New cases today", value = diseaseapi.format_number(data.today.cases))
    embed.add_field(name="Total deaths", value = diseaseapi.format_number(data.deaths))
    embed.add_field(name="New deaths today", value = diseaseapi.format_number(data.today.deaths))
    embed.add_field(name="Number of tests", value = diseaseapi.format_number(data.tests))

def generate_all_embed(embed, data):

    embed.add_field(name="Total recoveries", value = diseaseapi.format_number(data.recoveries))
    embed.add_field(name="Total critical cases", value = diseaseapi.format_number(data.critical))
    embed.add_field(name="Active cases", value = diseaseapi.format_number(data.active))
    embed.add_field(name="Last updated", value = diseaseapi.format_date(data.updated))

def generate_country_embed(embed, data, yesterdays_data):

    embed.add_field(name="New cases yesterday", value = diseaseapi.format_number(yesterdays_data.today.cases))
    embed.add_field(name="New deaths yesterday", value = diseaseapi.format_number(yesterdays_data.today.deaths))
    embed.add_field(name="Total recoveries", value = diseaseapi.format_number(data.recoveries))
    embed.add_field(name="Total critical cases", value = diseaseapi.format_number(data.critical))
    embed.add_field(name="Active cases", value = diseaseapi.format_number(data.active))
    embed.add_field(name="Cases per million people", value = diseaseapi.format_number(data.per_million.cases))
    embed.add_field(name="Deaths per million people", value = diseaseapi.format_number(data.per_million.deaths))
    embed.add_field(name="Last updated", value = diseaseapi.format_date(data.updated))
    embed.description = "**Country: {}**".format(data.name)
    embed.set_thumbnail(url=data.info.flag)

def generate_state_embed(embed, data, yesterday):

    embed.add_field(name="New cases yesterday", value = diseaseapi.format_number(yesterday.today.cases))
    embed.add_field(name="New deaths yesterday", value = diseaseapi.format_number(yesterday.today.deaths))
    embed.add_field(name="Active cases", value = diseaseapi.format_number(data.active))
    embed.description = "**State: {}**".format(data.name)


class Coronavirus(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        if not hasattr(self.bot, 'covid'): 
            self.diseaseapi = diseaseapi.Client()
            self.bot.covid = self.diseaseapi.covid19

    async def _jhucsse(self, country, province):
    
        data = await self.bot.covid.jhucsse()

        if country.lower() == 'uk':
            country = 'united kingdom'

        relevant = next(cp for cp in data if cp.country_name.lower() == country.lower()\
            and str(cp.province_name).lower() == province.lower())
        
        embed = discord.Embed(title="Coronavirus (COVID-19) stats", color=0x855182)
        embed.set_footer(text="These stats are what has been officially confirmed. It is possible that real figures are different.")
        embed.description = "**Country: {}**\n**Province: {}**".format(relevant.country_name, relevant.province_name)

        embed.add_field(name="Total cases", value = diseaseapi.format_number(relevant.confirmed_cases))
        embed.add_field(name="Total deaths", value = diseaseapi.format_number(relevant.deaths))
        embed.add_field(name="Total recoveries", value = diseaseapi.format_number(relevant.recoveries))
        embed.add_field(name="Active cases", value = diseaseapi.format_number(relevant.confirmed_cases-relevant.deaths-relevant.recoveries))
        embed.add_field(name="Last updated", value = diseaseapi.format_date(relevant.updated))
        return embed


    @cog_ext.cog_slash(name="covid", description="Shows COVID-19 statistics from around the world")
    async def coronavirus(self, ctx, country=None):
    
        if country is None:
            data = await self.bot.covid.all(allow_none=True)

        else:
            data = await self.bot.covid.country(country, allow_none=True)

        embed = discord.Embed(title="Coronavirus (COVID-19) stats", color=0x855182)
        embed.set_footer(text="These stats are what has been officially confirmed. It is possible that real figures are different.")

        generate_base_embed(embed, data)

        if isinstance(data, diseaseapi.covidstatistics.Global):
            generate_all_embed(embed, data)

        elif isinstance(data, diseaseapi.covidstatistics.Country):
            yesterdays_data = await self.bot.covid.country(country, yesterday=True, allow_none=True)
            generate_country_embed(embed, data, yesterdays_data)

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(
      name="covidtop", 
      description="Shows COVID-19 statistics for the top 15 countries around the world",
      options=[
        create_option(
          name="sort",
          description="Sort between deaths and cases",
          option_type=3,
          required=False,
          choices=[
            create_choice(
              name="Deaths",
              value="Deaths"
              ),
            create_choice(
              name="Cases",
              value="Cases"
              )
            ]
      )
      ]
    )
    async def coronavirusleaderboard(self, ctx, sort:str=None):
      dea="Death"
      cas="Case"
      dealower="death"
      caslower="case"

      if sort is None:
        data = await self.bot.covid.all_countries(sort="cases")

        embed = discord.Embed(title="COVID-19 leaderboard sorted by {}".format("cases"), description="", color=0x855182)
        embed.set_footer(text='These stats are what has been officially confirmed. It is possible that real figures are different.')

        for i in range(1,16): 
            country = data[i-1]
            name = country.name
            
            if country.cases is None:
                cases = 'Unknown'
            else:
                cases = diseaseapi.format_number(country.cases)
            if country.deaths is None:
                deaths = 'Unknown'
            else:
                deaths = diseaseapi.format_number(country.deaths)

            embed.description = '{}**{}. {}:** {} cases, {} deaths.\n'.format(
                embed.description, i, name, cases, deaths
            )
        
        await ctx.send(embed=embed)
      if sort==dea:
        data = await self.bot.covid.all_countries(sort="deaths")

        embed = discord.Embed(title="COVID-19 leaderboard sorted by {}".format("deaths"), description="", color=0x855182)
        embed.set_footer(text='These stats are what has been officially confirmed. It is possible that real figures are different.')

        for i in range(1,16): 
            country = data[i-1]
            name = country.name
            
            if country.cases is None:
                cases = 'Unknown'
            else:
                cases = diseaseapi.format_number(country.cases)
            if country.deaths is None:
                deaths = 'Unknown'
            else:
                deaths = diseaseapi.format_number(country.deaths)

            embed.description = '{}**{}. {}:** {} cases, {} deaths.\n'.format(
                embed.description, i, name, cases, deaths
            )
        
        await ctx.send(embed=embed)
      if sort==dealower:
        data = await self.bot.covid.all_countries(sort="deaths")

        embed = discord.Embed(title="COVID-19 leaderboard sorted by {}".format("deaths"), description="", color=0x855182)
        embed.set_footer(text='These stats are what has been officially confirmed. It is possible that real figures are different.')

        for i in range(1,16): 
            country = data[i-1]
            name = country.name
            
            if country.cases is None:
                cases = 'Unknown'
            else:
                cases = diseaseapi.format_number(country.cases)
            if country.deaths is None:
                deaths = 'Unknown'
            else:
                deaths = diseaseapi.format_number(country.deaths)

            embed.description = '{}**{}. {}:** {} cases, {} deaths.\n'.format(
                embed.description, i, name, cases, deaths
            )
        
        await ctx.send(embed=embed)
      if sort==cas:
        data = await self.bot.covid.all_countries(sort="cases")

        embed = discord.Embed(title="COVID-19 leaderboard sorted by {}".format("cases"), description="", color=0x855182)
        embed.set_footer(text='These stats are what has been officially confirmed. It is possible that real figures are different.')

        for i in range(1,16): 
            country = data[i-1]
            name = country.name
            
            if country.cases is None:
                cases = 'Unknown'
            else:
                cases = diseaseapi.format_number(country.cases)
            if country.deaths is None:
                deaths = 'Unknown'
            else:
                deaths = diseaseapi.format_number(country.deaths)

            embed.description = '{}**{}. {}:** {} cases, {} deaths.\n'.format(
                embed.description, i, name, cases, deaths
            )
        
        await ctx.send(embed=embed)
      if sort==caslower:
        data = await self.bot.covid.all_countries(sort="cases")

        embed = discord.Embed(title="COVID-19 leaderboard sorted by {}".format("cases"), description="", color=0x855182)
        embed.set_footer(text='These stats are what has been officially confirmed. It is possible that real figures are different.')

        for i in range(1,16): 
            country = data[i-1]
            name = country.name
            
            if country.cases is None:
                cases = 'Unknown'
            else:
                cases = diseaseapi.format_number(country.cases)
            if country.deaths is None:
                deaths = 'Unknown'
            else:
                deaths = diseaseapi.format_number(country.deaths)

            embed.description = '{}**{}. {}:** {} cases, {} deaths.\n'.format(
                embed.description, i, name, cases, deaths
            )
        
        await ctx.send(embed=embed)
      else:
        data = await self.bot.covid.all_countries(sort=sort.lower())

        embed = discord.Embed(title="COVID-19 leaderboard sorted by {}".format(sort.lower()), description="", color=0x855182)
        embed.set_footer(text='These stats are what has been officially confirmed. It is possible that real figures are different.')

        for i in range(1,16): 
            country = data[i-1]
            name = country.name
            
            if country.cases is None:
                cases = 'Unknown'
            else:
                cases = diseaseapi.format_number(country.cases)
            if country.deaths is None:
                deaths = 'Unknown'
            else:
                deaths = diseaseapi.format_number(country.deaths)

            embed.description = '{}**{}. {}:** {} cases, {} deaths.\n'.format(
                embed.description, i, name, cases, deaths
            )
        
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Coronavirus(bot))