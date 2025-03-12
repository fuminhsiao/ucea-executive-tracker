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
            reader = csv.DictReader(file)

            for row in reader:
                date = parse_date(row['Date']) if row['Date'] else None
                name_of_action = row['Name of Action']
                description = row['What It Says']
                meaning = row['What It Means']
                status = row['Status'] if row['Status'] else None
                source = row['Primary Source'] if row['Primary Source'] else None
                challenge_to_action = row['Challenges to Action'] if row['Challenges to Action'] else None
                news_commentary = row['News & Commentary'] if row['News & Commentary'] else None
                notes = row['Notes'] if row['Notes'] else None
                additional_info = row['Additional Info'] if row['Additional Info'] else None
                fallout = row['Fallout'] if row['Fallout'] else None

                # ✅ 處理 Type of Action (多選)
                type_of_action_names = row['Type of Action'].split(', ')
                type_of_actions = [TypeOfAction.objects.get_or_create(name=toa.strip())[0] for toa in type_of_action_names]

                # ✅ 處理 Actors (多選)
                actor_names = row['Actor/Authorizer'].split(', ')
                actors = [Actor.objects.get_or_create(name=actor.strip())[0] for actor in actor_names]

                # ✅ 處理 Topics (多選)
                topic_names = row['Topic'].split(', ')
                topics = [Topic.objects.get_or_create(name=topic.strip())[0] for topic in topic_names]

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
