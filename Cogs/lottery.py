import os
import glob
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
        self.mCounterList = {}  # 로또 숫자 별 추첨 횟수
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

    def delete_list(self, filename: str):
        for name in glob.glob(filename):
            print(name + "deleted")
            os.remove(name)

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

    # 다운받은 리스트를 통해 계산
    def calculate_list(self):
        if os.path.isfile(self.listFilePath):
            for idx in range(1, 46):
                self.mCounterList[str(idx)] = 0  # 리스트 초기화
            default_row = 3   # 로또 list 에서 추첨 번호가 시작 하는 행
            list_xml = open(self.listFilePath, encoding='cp949')  # 저장된 list 불러오기
            soup = BeautifulSoup(list_xml, 'html.parser')  # 데이터 파싱
            total_info = soup.findAll('tr')
            for row in range(default_row, len(total_info)):
                row_data = total_info[row].findAll('td')
                max_col = len(row_data)
                for col in range(max_col-7, max_col):
                    # 각 숫자가 뽑힌 횟수 계산
                    self.mCounterList[row_data[col].text] += 1
        else:
            self.download_total()
            self.calculate_list()


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

    @commands.command(name="계산")
    async def calc_list(self, ctx):
        msg = await ctx.send("계산시작")
        self.lottery.calculate_list()
        await msg.delete()
        embed = discord.Embed(title="로또 당첨번호 내역", description="번호별 당첨 횟수를 출력합니다")
        embed.add_field(name="내역", value=self.lottery.mCounterList, inline=True)
        await ctx.send("계산완료", embed=embed)


async def setup(app):
    await app.add_cog(Lottery(app))
