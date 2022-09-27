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
        self.listFilePath = ""
        self.mCounterList = {}  # 로또 숫자 별 추첨 횟수
        self.mCalculated = False  # 리스트에 대하여 계산여부 저장
        self.check_list()

    def check_list(self):
        self.parse_newest()
        self.download_total()
        self.calculate_list()

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
        self.listFilePath = f'./lottery{self.lastGameCount}.xls'

    def delete_list(self, filename: str):
        for name in glob.glob(filename):
            print(name + " 파일이 삭제되었습니다")
            os.remove(name)

    # 모든 추첨 번호 다운 로드
    def download_total(self):  # list 를 새로 다운받았을 경우 true 반환
        if os.path.isfile(self.listFilePath):
            print("최신 로또결과가 이미 존재합니다\n")
        else:
            self.delete_list('*[0-9].xls')
            start_count = 1
            url = f'https://dhlottery.co.kr/gameResult.do?method=allWinExel&gubun=byWin&nowPage=1&' \
                  f'drwNoStart={start_count}&drwNoEnd={self.lastGameCount}'
            urllib.request.urlretrieve(url, self.listFilePath)
            self.mCalculated = False

    # 다운받은 리스트를 통해 계산
    def calculate_list(self):
        if os.path.isfile(self.listFilePath):
            if not self.mCalculated:
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
                print("로또 번호 리스트 계산완료\n")
                self.mCalculated = True
        else:
            self.download_total()
            self.calculate_list()


class Lottery(commands.Cog):
    def __init__(self, app):
        self.app = app
        self.lottery = LotteryFunction()

    @commands.command(name="로또")
    async def lottery(self, ctx):
        self.lottery.check_list()
        embed = discord.Embed(title="로또 추첨 번호", description="최근 로또 번호를 출력합니다", colour=0xffffff)
        embed.set_thumbnail(url="https://dhlottery.co.kr/images/layout/logo-header.png")
        # 데이터로부터 추첨날짜 확인
        embed.add_field(name="추첨날짜", value=self.lottery.lastGameDate, inline=True)
        # 데이터로부터 회차 확인
        embed.add_field(name="회차", value=self.lottery.lastGameCount+"회", inline=True)
        embed.add_field(name="추첨번호", value=self.lottery.lastGameNumbers, inline=False)
        await ctx.send(embed=embed)


async def setup(app):
    await app.add_cog(Lottery(app))
