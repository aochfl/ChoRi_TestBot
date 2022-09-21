import os
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import urllib.request


class LotteryFunction:
    def __init__(self):
        self.lastGameCount = None  # 1033
        self.lastGameDate = None  # (2022년 09월 17일 추첨)
        self.lastGameNumbers = []
        self.parse_newest()
        self.listFilePath = f'./lottery{self.lastGameCount}.xls'

    # 현재 회차 정보 파싱
    def parse_newest(self):
        self.lastGameNumbers.clear()
        url = 'https://dhlottery.co.kr/gameResult.do?method=byWin'
        webpage = urllib.request.urlopen(url)
        soup = BeautifulSoup(webpage, 'html.parser')
        self.lastGameCount = soup.select_one('div.win_result > h4 > strong').get_text().split("회")[0]
        self.lastGameDate = soup.select_one('div.win_result > p').get_text()
        numberList = soup.select('div.win_result > div > .num > p .ball_645')
        for number in numberList:
            self.lastGameNumbers.append(number.get_text())

    # 모든 추첨 번호 다운 로드
    def download_total(self):
        if os.path.isfile(self.listFilePath):
            print("lottery list exist")
        else:
            self.delete_list('*[0-9].xls')
            start_count = 1
            url = f'https://dhlottery.co.kr/gameResult.do?method=allWinExel&gubun=byWin&nowPage=1&' \
                  f'drwNoStart={start_count}&drwNoEnd={self.lastGameCount}'
            urllib.request.urlretrieve(url, self.listFilePath)


class Lottery(commands.Cog):
    def __init__(self, app):
        self.app = app
        self.lottery = LotteryFunction()

    @commands.command(name="로또")
    async def lottery(self, ctx):
        self.lottery.parse_newest()
        embed = discord.Embed(title="로또 추첨 번호", description="최근 로또 번호를 출력합니다", colour=0xffffff)
        embed.set_thumbnail(url="https://dhlottery.co.kr/images/layout/logo-header.png")
        # 데이터로부터 추첨날짜 확인
        embed.add_field(name="추첨날짜", value=self.lottery.lastGameDate, inline=True)
        # 데이터로부터 회차 확인
        embed.add_field(name="회차", value=self.lottery.lastGameCount+"회", inline=True)
        embed.add_field(name="추첨번호", value=self.lottery.lastGameNumbers, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="다운")
    async def download_list(self, ctx):
        msg = await ctx.send("다운로드 시작")
        self.lottery.download_total()
        await ctx.message.delete()
        await msg.delete()
        await ctx.send("다운로드 완료", delete_after=5)


async def setup(app):
    await app.add_cog(Lottery(app))
