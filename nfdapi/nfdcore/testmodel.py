import reversion
from nfdcore.models import Voucher, OccurrenceTaxon, OccurrenceNaturalArea
from nfdcore.models import ElementSpecies, SRank
from reversion.models import Version

with reversion.create_revision():
    v = Voucher()
    v.voucher_number = 10
    v.specimen_collected = True
    v.parts_collected = True
    v.save()

with reversion.create_revision():    
    srank = SRank()
    srank.srank = "srank0"
    srank.save()
    
with reversion.create_revision():
    e = ElementSpecies()
    e.s_rank = srank
    e.name_sci = "Quercus suber"
    e.first_common = "Surera"
    e.second_common = "Alcornoque"
    e.save()

with reversion.create_revision():    
    t = OccurrenceTaxon()
    t.species = e
    t.voucher = v
    t.save()
    

versions = Version.objects.get_for_object(v)
print len(versions)
print versions[0].field_dict["voucher_number"]

with reversion.create_revision():
    v.voucher_number = 11
    v.parts_collected = False
    v.save()

versions = Version.objects.get_for_object(v)
print len(versions)

with reversion.create_revision():
    v.voucher_number = 12
    v.parts_collected = True
    v.save()
    
#vt = Version.objects.get_for_object(t).filter(revision__date_created__lte=datetime.datetime(2017, 5, 25, 14, 40, 0, 0))
vall = Voucher.objects.all()
v1 = vall[0]
v2 = vall[1]
ver = Version.objects.get_for_object(v2)
