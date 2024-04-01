import django_tables2 as tables
from .serializers import LeaderBoardSerializer

class LeaderBoard(tables.Table):
    id = tables.Column()
    username = tables.Column()
    total_score = tables.Column()

    class Meta:
        template_name = "django_tables2/bootstrap5.html"