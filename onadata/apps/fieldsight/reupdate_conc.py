


from onadata.apps.fsforms.models import *
from onadata.apps.viewer.models.parsed_instance import update_mongo_instance


def replace_data(form_id, query_key, query_value, data):
	mongo_ids=settings.MONGO_DB.instances.aggregate([{'$match': {'fs_project_uuid':str(form_id), query_key : query_value}},
													 {'$project':{'_id':1}}], cursor={})
	mongo_ids = list(mongo_ids)
	ids = []
	for mongo_id in mongo_ids['result']:
		ids.append(mongo_id['_id'])
	
	instances = Instance.objects.filter(id__in=ids)
	instance_ids = []	
 
	for instance in instances:
		instance_ids.append(instance.id)		
		for key, value in data.items():
			print instance.id
			print key, "------", instance.json.get(key, None)	
			instance.json[key] = value		
			print key, ">>>>>>",instance.json[key]
			print "::::::"

		events = instance.json[query_key].split(" ")		
		if query_value in events:
			events.remove(query_value)		
		new_event = ""			
		for event in events:
			new_event = new_event + event + " "
		instance.json[query_key] = new_event
		
		instance.save(hack=True)

		d = instance.parsed_instance.to_dict_for_mongo()
		for key, value in instance.json.items():
			d[key] = value	
		
		d.update({'fs_project_uuid': str(instance.fieldsight_instance.project_fxf_id), 'fs_project': instance.fieldsight_instance.project_id, 'fs_status': instance.fieldsight_instance.form_status, 'fs_site':str(instance.fieldsight_instance.site_id), 'fs_uuid':str(instance.fieldsight_instance.site_fxf_id)})
		update_mongo_instance(d)
		

replace_data(1422297, 'event_type', 'ward_level_mee', {'event_type':'stakeholder_meeting', 'topic_meeting':'ward_level_mee'})

replace_data(1422297, 'event_type', 'municipality_l', {'event_type':'stakeholder_meeting', 'topic_meeting':'municipality_l'})

replace_data(1422297, 'event_type', 'recons_com', {'event_type':'stakeholder_meeting', 'topic_meeting':'recons_com'})

replace_data(1422297, 'event_type', 'ojt_training', {'event_type':'training', 'topic_training':'ojt_training'})

replace_data(1422297, 'event_type', 'homeowner_training', {'event_type':'training', 'topic_training':'homeowner_training'})

replace_data(1422297, 'event_type', 'engineer_training', {'event_type':'training', 'topic_training':'engineer_training'})




#########################################################


instance = Instance.objects.get(pk=81187)
instance.json['event_details/pa_num'] ="28-40-8-0-30, 28-40-8-0-31, 28-40-8-0-65, 28-40-8-0-21, 28-40-8-0-70, 28-40-8-0-78, 28-40-8-0-68, 28-40-8-0-76, 28-40-8-0-21, 28-40-8-0-02, 28-40-8-0-79, 28-40-8-0-62."
instance.json.pop('event_details/pa_num10')
instance.json.pop('event_details/pa_num11')

instance = Instance.objects.get(pk=78968)
instance.json.pop('topic_meeting')
instance.json['topic_training'] = "engineer_training"


instances = Instance.objects.filter(fieldsight_instance__project_fxf_id=1422297)
for instance in instances:
	data_split = instance.json.get('event_details/pa_num', '').split(",")
	if len(data_split) > 1:
		ids.append(instance.id)
		count = 0
		print instance.json['event_details/pa_num']
	
		for i in data_split:
			if count == 0:
				instance.json['event_details/pa_num'] = i
				print 'event_details/pa_num', i
			elif count > 9:
				instance.json['event_details/pa_num9'] = instance.json['event_details/pa_num9'] + ',' + i
			else:
				instance.json['event_details/pa_num'+str(count)] = i
				print 'event_details/pa_num'+str(count), i

			count+=1

		print "==========================="
		instance.save(hack=True)

		d = instance.parsed_instance.to_dict_for_mongo()
		for key, value in instance.json.items():
			d[key] = value	
		
		d.update({'fs_project_uuid': str(instance.fieldsight_instance.project_fxf_id), 'fs_project': instance.fieldsight_instance.project_id, 'fs_status': instance.fieldsight_instance.form_status, 'fs_site':str(instance.fieldsight_instance.site_id), 'fs_uuid':str(instance.fieldsight_instance.site_fxf_id)})
		update_mongo_instance(d)




###############################################





mongo_ids=settings.MONGO_DB.instances.aggregate([{'$match': {'fs_project_uuid':"992794", 'visit_purpose': {'$regex' : 'drawing_regist'}}}, {'$project':{'_id':1, 'drawing_regist':1, 'visit_purpose':1}}], cursor={})
ids=[]
mongo_ids = list(mongo_ids)
if mongo_ids['result']:
	for mongo_id in mongo_ids['result']:
		ids.append(mongo_id['_id'])
		
	instances = Instance.objects.filter(id__in=ids)

	for instance in instances:
		data = instance.json['visit_purpose']
		data_split = data.split(' ')
		if not 'drawing' in data_split:
			if data == "":
				new_data = 'drawing'
			else:
				new_data = data + ' drawing'		
					
			instance.json['visit_purpose'] = new_data

		
		instance.json['drawing_purpose'] = 'drawing_regist'
		
		events = instance.json['visit_purpose'].split(" ")		
		if 'drawing_regist' in events:
			events.remove('drawing_regist')		
		new_event = ""			
		for event in events:
			if new_event == "":
				new_event = event
			else:
				new_event = new_event + " " + event
		instance.json['visit_purpose'] = new_event

		instance.save(hack=True)

		print instance.json['drawing_purpose'], instance.json['visit_purpose']		

		d = instance.parsed_instance.to_dict_for_mongo()
		for key, value in instance.json.items():
			d[key] = value	
		d = instance.parsed_instance.to_dict_for_mongo()
		d.update({'fs_project_uuid': str(instance.fieldsight_instance.project_fxf_id), 'fs_project': instance.fieldsight_instance.project_id, 'fs_status': instance.fieldsight_instance.form_status, 'fs_site':str(instance.fieldsight_instance.site_id), 'fs_uuid':str(instance.fieldsight_instance.site_fxf_id)})
		update_mongo_instance(d)
		



#########################################################



mongo_ids=settings.MONGO_DB.instances.aggregate([{'$match': {'fs_project_uuid':"992794", 'visit_purpose': {'$regex' : 'drawing_receiv'}}}, {'$project':{'_id':1, 'visit_purpose':1}}], cursor={})
ids=[]
mongo_ids = list(mongo_ids)
if mongo_ids['result']:
	for mongo_id in mongo_ids['result']:
		ids.append(mongo_id['_id'])
		
	instances = Instance.objects.filter(id__in=ids)

	for instance in instances:
		data = instance.json['visit_purpose']
		data_split = data.split(' ')
				
		if not 'drawing' in data_split:
			if data == "":
				new_data = 'drawing'
			else:
				new_data = data + ' drawing'		
					
			instance.json['visit_purpose'] = new_data
		
		instance.json['drawing_purpose'] = 'drawing_receiv'

		events = instance.json['visit_purpose'].split(" ")		
		if 'drawing_receiv' in events:
			events.remove('drawing_receiv')		
		new_event = ""			
		for event in events:
			if new_event == "":
				new_event = event
			else:
				new_event = new_event + " " + event

		instance.json['visit_purpose'] = new_event

		print instance.json['visit_purpose'], "--------", instance.json['drawing_purpose']

		instance.save(hack=True)

		d = instance.parsed_instance.to_dict_for_mongo()
		for key, value in instance.json.items():
			d[key] = value	
		d.update({'fs_project_uuid': str(instance.fieldsight_instance.project_fxf_id), 'fs_project': instance.fieldsight_instance.project_id, 'fs_status': instance.fieldsight_instance.form_status, 'fs_site':str(instance.fieldsight_instance.site_id), 'fs_uuid':str(instance.fieldsight_instance.site_fxf_id)})
		
		update_mongo_instance(d)
		




#########################################################



mongo_ids=settings.MONGO_DB.instances.aggregate([{'$match': {'fs_project_uuid':"992794", 'visit_purpose':  {'$regex' : 'project_inquir'}}}, {'$project':{'_id':1, 'visit_purpose':1}}], cursor={})
ids=[]
mongo_ids = list(mongo_ids)
if mongo_ids['result']:
	for mongo_id in mongo_ids['result']:
		ids.append(mongo_id['_id'])
		
		instances = Instance.objects.filter(id__in=ids)

	for instance in instances:
		data = instance.json['visit_purpose']
		data_split = data.split(' ')

		if not 'consultation' in data_split:
			if data == "":
				new_data = 'consultation'
			else:
				new_data = data + ' consultation'
			instance.json['visit_purpose'] = new_data
		
		cdata = instance.json.get('consultation_type','')
		cdata_split = cdata.split(' ')

		if not 'project_inquir' in cdata_split:
			if cdata == "":
				instance.json['consultation_type'] = 'project_inquir'
			else:
				instance.json['consultation_type'] = cdata + ' project_inquir'
		

		events = instance.json['visit_purpose'].split(" ")		
		if 'project_inquir' in events:
			events.remove('project_inquir')		
		new_event = ""			
		for event in events:
			if new_event == "":
				new_event = event
			else:
				new_event = new_event + " " + event

		instance.json['visit_purpose'] = new_event


		print instance.json['visit_purpose'], " ---- ", instance.json['consultation_type']
		


		instance.save(hack=True)

		d = instance.parsed_instance.to_dict_for_mongo()
		for key, value in instance.json.items():
			d[key] = value		

		d = instance.parsed_instance.to_dict_for_mongo()
		d.update({'fs_project_uuid': str(instance.fieldsight_instance.project_fxf_id), 'fs_project': instance.fieldsight_instance.project_id, 'fs_status': instance.fieldsight_instance.form_status, 'fs_site':str(instance.fieldsight_instance.site_id), 'fs_uuid':str(instance.fieldsight_instance.site_fxf_id)})
		update_mongo_instance(d)
		



#########################################################



mongo_ids=settings.MONGO_DB.instances.aggregate([{'$match': {'fs_project_uuid':"992794", 'consultation_type': {'$regex' : 'trained_masons'}}}, {'$project':{'_id':1, 'consultation_type':1}}], cursor={})

ids=[]
mongo_ids = list(mongo_ids)
if mongo_ids:
	for mongo_id in mongo_ids['result']:
		ids.append(mongo_id['_id'])
		
		instances = Instance.objects.filter(id__in=ids)

	for instance in instances:
		data = instance.json['visit_purpose']
		data_split = data.split(' ')

		if not 'consultation' in data_split:
			if data == "":
				instance.json['visit_purpose'] = 'consultation'
			else:
				instance.json['visit_purpose'] = data + ' consultation'
		
		cdata = instance.json.get('consultation_type', '')
		cdata_split = cdata.split(' ')

		if not 'const_method' in cdata_split:
			if cdata == "":
				instance.json['consultation_type'] = 'const_method'
			else:
				instance.json['consultation_type'] = cdata + ' const_method'
		

		ccdata = instance.json.get('consultation_const', '')
		ccdata_split = ccdata.split(' ')

		if not 'manpower' in ccdata_split:
			if ccdata == "":
				instance.json['consultation_const'] = 'manpower'
			else:
				instance.json['consultation_const'] = ccdata + ' manpower'

		cccdata = instance.json.get('const_manager', '')
		cccdata_split = cccdata.split(' ')

		if not 'trained_mason' in cccdata_split:
			instance.json['const_manager'] = 'trained_mason'
		else:
			instance.json['const_manager'] = cccdata + ' trained_mason'


		events = instance.json['consultation_type'].split(" ")		
		if 'trained_masons' in events:
			events.remove('trained_masons')		
		new_event = ""			
		for event in events:
			if new_event == "":
				new_event = event
			else:
				new_event = new_event + " " + event
		instance.json['consultation_type'] = new_event


		print instance.json['consultation_const'], "  ",instance.json['consultation_type']+"  ",instance.json['visit_purpose']


		instance.save(hack=True)

		d = instance.parsed_instance.to_dict_for_mongo()
		for key, value in instance.json.items():
			d[key] = value	

		d = instance.parsed_instance.to_dict_for_mongo()
		d.update({'fs_project_uuid': str(instance.fieldsight_instance.project_fxf_id), 'fs_project': instance.fieldsight_instance.project_id, 'fs_status': instance.fieldsight_instance.form_status, 'fs_site':str(instance.fieldsight_instance.site_id), 'fs_uuid':str(instance.fieldsight_instance.site_fxf_id)})
		update_mongo_instance(d)
		


#########################################################



mongo_ids=settings.MONGO_DB.instances.aggregate([{'$match': {'fs_project_uuid':"992794", 'mun_report_type': {'$regex' : 'building_permit'}}}, {'$project':{'_id':1, 'mun_report_type':1}}], cursor={})
ids=[]
mongo_ids = list(mongo_ids)
if mongo_ids:
	for mongo_id in mongo_ids:
		ids.append(mongo_id['_id'])
		
	instances = Instance.objects.filter(id__in=ids)
	print instances.count()
	for instance in instances:
		data = instance.json['mun_report_type']
		data_split = data.split(' ')

		if not 'permit_report' in data_split:
			
			if data == "":
				data = 'permit_report'
			else:
				data = data + ' ' +'permit_report'
				
			instance.json['mun_report_type'] = data
		
		
		events = instance.json['mun_report_type'].split(" ")		
		if 'building_permit' in events:
			events.remove('building_permit')		
		new_event = ""			
		for event in events:
			if new_event == "":
				new_event = event
			else:
				new_event = new_event + " " + event
		instance.json['mun_report_type'] = new_event

		
		cdata = instance.json.get('building_report_type', '')
		cdata_split = cdata.split(' ')


		if not 'building_permit' in cdata_split:
			
			
			if cdata == "":
				cnew_data = 'building_permit'
			else:
				cnew_data = cdata + ' building_permit'
					
				
			instance.json['building_report_type'] = cnew_data
		


		print instance.json['mun_report_type'], "  ",instance.json['building_report_type'], instance.json['visit_purpose'] 
		

		
		instance.save(hack=True)

		d = instance.parsed_instance.to_dict_for_mongo()
		for key, value in instance.json.items():
			d[key] = value	
		
		d.update({'fs_project_uuid': str(instance.fieldsight_instance.project_fxf_id), 'fs_project': instance.fieldsight_instance.project_id, 'fs_status': instance.fieldsight_instance.form_status, 'fs_site':str(instance.fieldsight_instance.site_id), 'fs_uuid':str(instance.fieldsight_instance.site_fxf_id)})
		update_mongo_instance(d)



#########################################################



mongo_ids=settings.MONGO_DB.instances.aggregate([{'$match': {'fs_project_uuid':"992794", 'mun_report_type': {'$regex' : 'completion_certificate'}}}, {'$project':{'_id':1, 'mun_report_type':1}}], cursor={})
ids=[]
mongo_ids = list(mongo_ids)
if mongo_ids:
	for mongo_id in mongo_ids:
		ids.append(mongo_id['_id'])
		
		instances = Instance.objects.filter(id__in=ids)

	for instance in instances:
		print instance.id
		data = instance.json['mun_report_type']
		data_split = data.split(' ')

		if not 'permit_report' in data_split:
			if data == "":
				instance.json['mun_report_type'] = 'permit_report'
			else:
				instance.json['mun_report_type'] = data + ' permit_report'
		

		events = instance.json['mun_report_type'].split(" ")		
		if 'completion_certificate' in events:
			events.remove('completion_certificate')		
		new_event = ""			
		for event in events:
			if new_event == "":
				new_event = event
			else:
				new_event = new_event + " " + event

		instance.json['mun_report_type'] = new_event
		print new_event, "-----"


		cdata = instance.json.get('building_report_type', "")
		cdata_split = cdata.split(' ')

		if not 'completion_certificate' in cdata_split:
			
			if cdata == "":
				cnew_data = 'completion_certificate'
			else:
				cnew_data = cdata + ' completion_certificate'
					
				
			instance.json['building_report_type'] = cnew_data
		

		

		print instance.json['mun_report_type'],"---", instance.json['building_report_type'], instance.json['visit_purpose'] 
		

		instance.save(hack=True)

		d = instance.parsed_instance.to_dict_for_mongo()
		for key, value in instance.json.items():
			d[key] = value	
		d.update({'fs_project_uuid': str(instance.fieldsight_instance.project_fxf_id), 'fs_project': instance.fieldsight_instance.project_id, 'fs_status': instance.fieldsight_instance.form_status, 'fs_site':str(instance.fieldsight_instance.site_id), 'fs_uuid':str(instance.fieldsight_instance.site_fxf_id)})
		print d, "---"
		update_mongo_instance(d)
	
