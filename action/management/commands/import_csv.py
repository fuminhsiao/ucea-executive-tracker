import csv
import os
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from action.models import Action, TypeOfAction, Actor, Topic

class Command(BaseCommand):
    help = 'Import Actions from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help="Path to the CSV file")

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)  # 先用普通 reader 讀取
            next(reader)  # ✅ 跳過第一行
            headers = next(reader)  # ✅ 第二行當作標題

            # ✅ 重新用 DictReader 讀取數據，並設定標題
            reader = csv.DictReader(file, fieldnames=headers)

            for row in reader:
                date = parse_date(row['Date']) if row.get('Date') else None
                name_of_action = row.get('Name of Action', '').strip()
                description = row.get('What It Says', '').strip()
                meaning = row.get('What It Means', '').strip()
                status = row.get('Status', '').strip() or None
                source = row.get('Primary Source', '').strip() or None
                challenge_to_action = row.get('Challenges to Action', '').strip() or None
                news_commentary = row.get('News & Commentary', '').strip() or None
                notes = row.get('Notes', '').strip() or None
                additional_info = row.get('Additional Info', '').strip() or None
                fallout = row.get('Fallout', '').strip() or None

                # ✅ 處理 Type of Action (多選)
                type_of_action_names = row.get('Type of Action', '').split(', ')
                type_of_actions = [TypeOfAction.objects.get_or_create(name=toa.strip())[0] for toa in type_of_action_names if toa]

                # ✅ 處理 Actors (多選)
                actor_names = row.get('Actor/Authorizer', '').split(', ')
                actors = [Actor.objects.get_or_create(name=actor.strip())[0] for actor in actor_names if actor]

                # ✅ 處理 Topics (多選)
                topic_names = row.get('Topic', '').split(', ')
                topics = [Topic.objects.get_or_create(name=topic.strip())[0] for topic in topic_names if topic]

                # ✅ 創建 Action 物件
                action = Action.objects.create(
                    date=date,
                    name_of_action=name_of_action,
                    description=description,
                    meaning=meaning,
                    status=status,
                    source=source,
                    challenge_to_action=challenge_to_action,
                    news_commentary=news_commentary,
                    notes=notes,
                    additional_info=additional_info,
                    fallout=fallout
                )

                # ✅ 添加 ManyToMany 關係
                action.type_of_action.set(type_of_actions)
                action.actors.set(actors)
                action.topics.set(topics)

        self.stdout.write(self.style.SUCCESS("✅ CSV Data Imported Successfully!"))
