from execo import *
from execo_g5k import *
import requests
import json
import config
import datetime


class Helper ():
    def __init__(self):
        pass
    
    @classmethod
    def AllocDeployG5k(self,NbNodes,walltime,job_name):
        logger.info('Find Resources')
        maxNode=0
        hosts =[]
        NbNodes = int (NbNodes)
        start = datetime.datetime.now()
        default_connection_params['user'] = 'root'
        #sites = ['lyon', 'rennes','grenoble', 'lille','nancy','nantes']
        sites = ['nantes']
        #sites = get_g5k_sites()
        planning = get_planning(sites)
        #blacklisted = ['lyon']
        slots = compute_slots(planning, walltime)
        wanted = {'grid5000': NbNodes}
        print("******* Max **********")
        start_date, end_date, resources = find_max_slot(slots, wanted)
        print(start_date)
        print(end_date)    
        print(resources)  
    
        #print("********** First **********") 
        #start_date, end_date, resources = find_first_slot(slots, wanted)
        #print(start_date)
        #print(end_date)    
        #print(resources)
        
        #print("************* Free ***********") 
        #start_date, end_date, resources = find_first_slot(slots, wanted)
        #print(start_date)
        #print(end_date)    
        #print(resources)
       
        for c in filter(lambda x: x in get_g5k_clusters(), resources.keys()):
            if resources[c] > NbNodes :
                if(resources[c]>maxNode):
                    maxNode = resources[c]
                    wanted = {c: NbNodes}                 
        jobs_specs = get_jobs_specs(wanted, name=job_name)
        end = datetime.datetime.now()
        print(end - start)
        totalTime = (end - start)
        logger.info('Resource Allocation')
        start = datetime.datetime.now()
        for sub, frontend in jobs_specs:              
            sub.walltime = walltime
            sub.job_type = "deploy"
        job = oarsub(jobs_specs)[0]
        end = datetime.datetime.now()
        print(end - start)
        totalTime = totalTime +(end - start)
        logger.info('Getting Reserved Nodes')
        start = datetime.datetime.now()
        print(job[0])
        print(job[1])
        nodes = get_oar_job_nodes(job[0], job[1])
        end = datetime.datetime.now()
        print(end - start)
        totalTime = totalTime +(end - start)
        logger.info('Deploying hosts')
        print(nodes)
        start = datetime.datetime.now()
        deployed, undeployed = deploy(Deployment(nodes, env_name="aevol_env2"))
        end = datetime.datetime.now()

        print(end - start)
        totalTime = totalTime +(end - start)
        for node in nodes :
            hosts.append(node.address)
        print(hosts)
        print(totalTime)
        return hosts,totalTime,job[0],job[1]
    @classmethod
    def SiteList(self):
        sites =[]
        r = requests.get(config.G5K_API_BASE_URL+'/sites/', auth=(config.G5K_LOGIN ,config.G5K_PASSWORD))
        json_data = json.loads(r.text)
        items =json_data['items']
        for item in items :
            sites.append(item['name'])
        return sites

    @classmethod
    def reservationsSites(self):
        reservationList =[]
        sites = self.SiteList()
        #print(sites)
        for site in sites :
            s = site.split("-")
            site =s[0]
            reservations =0
            r = requests.get(config.G5K_API_BASE_URL+'/sites/'+site.lower()+'/status', auth=(config.G5K_LOGIN ,config.G5K_PASSWORD))         
            json_data = json.loads(r.text)
            nodes= json_data['nodes']
            for nodeName in nodes :
                node=nodes[nodeName]             
                reservations= reservations + len(node['reservations'])
            reservationList.append(reservations)
        return reservationList
    @classmethod
    def clusterList(self):
        result=[]
        sites = self.SiteList()
        for site in sites:
            s = site.split("-")
            site =s[0]
            r =requests.get(config.G5K_API_BASE_URL+'/sites/'+site.lower()+'/clusters/', auth=(config.G5K_LOGIN ,config.G5K_PASSWORD))
            json_data = json.loads(r.text)
            items = json_data['items']             
            clusters=[]    
            for item in items :    
                clusters.append(item['uid'])
            result.append({
                "site":site,
                "clusters" :clusters})
        return result
            
    """ 
    def nodesPerSite(self):
        siteCluster = self.clusterList()
        nbNodes =0 
        nodesSite =[]    
        for item in siteCluster :
            for cluster in item['clusters']:
                r =requests.get(config.G5K_API_BASE_URL+'/sites/'+item['site'].lower()+'/clusters/'+cluster+'/nodes/', auth=(config.G5K_LOGIN ,config.G5K_PASSWORD))
                json_data = json.loads(r.text)
                #print(json_data['total'])
                nbNodes = nbNodes + int(json_data['total'])
            nodesSite.append(nbNodes)
            nbNodes =0
        return nodesSite
    """
    @classmethod
    def nodesPerSite(self):
        groupedHosts = group_hosts(get_g5k_hosts())
    
        nbNodes =0
        nodesSite =[]
        for site in groupedHosts :
            siteContent = groupedHosts[site]         
            for cluster in siteContent :
                cluserContent =siteContent[cluster]
                nbNodes = nbNodes +len(cluserContent)
            nodesSite.append(nbNodes)
            nbNodes =0    
        return nodesSite

    @classmethod
    def pickSite(self):
        usageRates =[]
        pickedSite =""
        rate =0
        rateMin =1000
        i=0
        sites = self.SiteList()
        reservations = self.reservationsSites()

        nodeSites = self.nodesPerSite()
        for site in sites :
            rate =reservations[i]/nodeSites[i]
            usageRates.append(rate)
            if (rate<rateMin):
                rateMin =rate
                pickedSite = site
            i = i+1
        print(pickedSite)
        return pickedSite,usageRates,usageRates
        
    @classmethod
    def removeResources(self,job_id,frontend):
        logger.info('Destroying job %s on %s', job_id,frontend)
        result=oardel([(int(job_id),frontend)])
        print(result)
        return  0


            
