"""
A management command which Grabs MPs Images from OA

"""

from django.core.management.base import NoArgsCommand
from members.models import *
from BeautifulSoup import BeautifulStoneSoup as BS
import urllib2
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

class Command(NoArgsCommand):
    help = "Grab All Members Images and Add them Into the DB"

    def handle_noargs(self, **options):        
        for mp in Member.objects.all():
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urllib2.urlopen("data.openaustralia.org/members/images/mps/" + str(mp.oa_id)).read())
            img_temp.flush()

            mp.simage.save(str(mp.id) + "S", File(img_temp))

            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urllib2.urlopen("data.openaustralia.org/members/images/mpsL/" + str(mp.oa_id)).read())
            img_temp.flush()

            mp.bimage.save(str(mp.id) + "B", File(img_temp))


