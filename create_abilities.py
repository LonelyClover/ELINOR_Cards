from httplib2 import Http
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from subprocess import run, DEVNULL
from tools.control import Main

def get_service():
  credentials_file = 'default/credentials.json'
  scopes = ['https://www.googleapis.com/auth/spreadsheets']

  credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scopes)

  http_auth = credentials.authorize(Http())
  service = build('sheets', 'v4', http=http_auth)

  return service

def get_spreadsheet():
  service = get_service()
  spreadsheet_id = '1kj-1-i6slaAfYQN1Auk81fCHuRlWmExKhBKSWzikPGM'
  ranges = ['Навыки!A1:G2']

  result = service.spreadsheets().values().batchGet(spreadsheetId=spreadsheet_id, ranges=ranges).execute()

  return result['valueRanges'][0]['values']

def generate_exp(location_name: str, cost: str):
  run(['python', 'create_exp.py'], stdout=DEVNULL,
      input=f'{location_name}\n{cost}\n', encoding='utf-8')
  

def generate_card(text: str, ability_level: str):
  if text == '':
    return

  lines = text.split('\n')

  ability_name = lines[0]
  ability_text = lines[1]

  with open('files/card.txt', 'w', encoding='utf-8') as f:
    f.write(ability_name + '\n')

    f.write('Навык\n')

    f.write(ability_level + '\n')

    f.write(ability_text)

  run(['python', 'create_card.py'], stdout=DEVNULL,
      input='2\n2\n', encoding='utf-8')


def generate_labels(location_name: str, names: list[str], amounts: list[int]):
  labels = [name for name, amount in zip(names, amounts) for _ in range(amount)]

  if len(labels) % 6 != 0:
    labels += [' '] * (len(labels) % 6)

  n = len(labels) // 6
  for i in range(n):
    current_labels = labels[i*6:(i+1)*6]

    with open('files/labels.txt', 'w', encoding='utf-8') as f:
      f.write('\n'.join(current_labels))

    run(['python', 'create_label.py'], stdout=DEVNULL,
        input=f'2\n{location_name} {i+1}\n', encoding='utf-8')


def generate_table(location_name: str, texts: list[str], levels: list[str]):
  with open("files/table.csv", "w", encoding="utf-8") as f:
    f.write('|'.join(levels) + '\n')
    
    f.write('|'.join([text.replace('\n', '\\n') for text in texts]) + '\n')

  run(['python', 'create_table.py'], stdout=DEVNULL,
      input=f'{location_name}\n', encoding='utf-8')
  

@Main
def create_abilities():
  print('Получение данных: ----', end='\r')
  spreadsheet = get_spreadsheet()
  print('Получение данных: DONE')

  print('Генерация файлов:')

  levels = spreadsheet[0][1:]

  for row in spreadsheet[1:]:
    location_name = row[0]
    
    print(f'{location_name:>20}:', end='\r')

    for i, cost in enumerate(['1', '3', '5']):
      print(f'{location_name:>20}:    Опыт: {str(i+1) + "/3":<5}', end='\r')
      generate_exp(location_name, cost)

    texts = row[1:]
    for i, text in enumerate(texts):
      print(f'{location_name:>20}:    Опыт: DONE     Навыки: {str(i+1) + "/" + str(len(texts)):<5}', end='\r')
      generate_card(text, levels[i])

    print(f'{location_name:>20}:    Опыт: DONE     Навыки: DONE     Наклейки: ----', end='\r')
    generate_labels(location_name,
                    [text.split('\n')[0] for text in texts],
                    [2 if level == 'I' else 1 for level in levels])

    print(f'{location_name:>20}:    Опыт: DONE     Навыки: DONE     Наклейки: DONE     Таблица: ----', end='\r')
    generate_table(location_name, texts, levels)

    print(f'{location_name:>20}:    Опыт: DONE     Навыки: DONE     Наклейки: DONE     Таблица: DONE')
