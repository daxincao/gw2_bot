'''
Takes a large list of items and returns pricing information for each item;
Writes pricing information into table


Divide each task into a batch of 200 items (limit for a single api query)
'''
import class_api_listings as al
import threading
import logging
import time
import sample_list as sl # 1233 test items
		

def worker(batch):
	logger.info('Starting')
	return_batch = al.get_listing_dataframe(batch)
	logger.debug(return_batch)
	logger.info("%s threads remaining" % threading.active_count())
	logger.info('Exiting')		

def batch_maker(large_list, n):
	'''
	Generator function for creating batches; returns a batch of items of size <= n
	'''
	while len(large_list) > 0:
		batch = large_list[:n]
		yield batch
		large_list = large_list[n:] 			
			

if __name__ == '__main__':
	
	logging.basicConfig(level=logging.INFO,
				format='[%(levelname)s] (%(threadName)-10s) %(message)s'
				)	
				
	logger = logging.getLogger(__name__)
	
	# Generate batches of 200
	batches = batch_maker(sl.sample_list, 200)
	
	# Start threading
	for batch in batches:
		w = threading.Thread(target=worker, args=(batch,))
		w.start()


		
	
	
	
