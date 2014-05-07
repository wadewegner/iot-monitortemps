list<Readings__c> DeleteList = [select Name from Readings__c limit 5000]; 

delete DeleteList;