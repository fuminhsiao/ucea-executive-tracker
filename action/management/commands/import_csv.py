import csv
import os
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from action.models import Action, TypeOfAction, Actor, Topic

class Command(BaseCommand):
    help = 'Import Actions from a CSV file without duplicating existing entries'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help="Path to the CSV file")

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                date = parse_date(row['Date']) if row['Date'] else None
                name_of_action = row['Name of Action']
                description = row['What It Says']
                meaning = row['What It Means']
                status = row['Status'] if row['Status'] else None
                source = row['Primary Source'] if row['Primary Source'] else None
                challenge_to_action = row['Challenges to Action'] if row['Challenges to Action'] else None
                challenge_link = row['Challenge Link'] if row['Challenge Link'] else None
                
                # ✅ 更新 `news_commentary` 相關欄位
                news_title = row['News & Commentary'] if row['News & Commentary'] else None
                news_link = row['News Link'] if row['News Link'] else None

                notes = row['Notes'] if row['Notes'] else None
                additional_info = row['Additional Info'] if row['Additional Info'] else None
                fallout = row['Fallout'] if row['Fallout'] else None

                # ✅ 檢查資料庫是否已經存在相同的 `name_of_action`
                action, created = Action.objects.update_or_create(
                    name_of_action=name_of_action,  # 以標題為主鍵，避免重複
                    defaults={
                        'date': date,
                        'description': description,
                        'meaning': meaning,
                        'status': status,
                        'source': source,
                        'challenge_to_action': challenge_to_action,
                        'challenge_link': challenge_link,
                        'news_title': news_title,  # ✅ 新增標題
                        'news_link': news_link,  # ✅ 新增超連結
                        'notes': notes,
                        'additional_info': additional_info,
                        'fallout': fallout
                    }
                )

                # ✅ 處理 Type of Action (多選)
                type_of_action_names = row['Type of Action'].split(', ')
                type_of_actions = [TypeOfAction.objects.get_or_create(name=toa.strip())[0] for toa in type_of_action_names]

                # ✅ 處理 Actors (多選)
                actor_names = row['Actor/Authorizer'].split(', ')
                actors = [Actor.objects.get_or_create(name=actor.strip())[0] for actor in actor_names]

                # ✅ 處理 Topics (多選)
                topic_names = row['Topic'].split(', ')
                topics = [Topic.objects.get_or_create(name=topic.strip())[0] for topic in topic_names]

                # ✅ 更新 ManyToMany 關係
                action.type_of_action.set(type_of_actions)
                action.actors.set(actors)
                action.topics.set(topics)

                # ✅ 提示是新建還是更新
                if created:
                    self.stdout.write(self.style.SUCCESS(f"✅ 新增: {name_of_action}"))
                else:
                    self.stdout.write(self.style.WARNING(f"🔄 更新: {name_of_action}"))

        self.stdout.write(self.style.SUCCESS("🚀 CSV Data Imported & Updated Successfully!"))
