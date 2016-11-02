
library(rvest)
library(ggplot2)
library(stringr)
library(jsonlite)
library(ggiraph)
library(dplyr)


start_dt = '2016-10-01'
end_dt = '2016-10-31'
query_str = 'naver'

days <- seq(from=as.Date(start_dt), to=as.Date(end_dt),by='days' )
date_v = c()
title_v = c()
for ( i in seq_along(days) )
{
  
  url = paste("http://news.naver.com/main/search/search.nhn?query=",query_str,"&st=news.all&q_enc=EUC-KR&r_enc=UTF-8&r_format=xml&rp=none&sm=title.basic&ic=all&so=rel.dsc&detail=1&pd=4&r_cluster2_start=1&r_cluster2_display=10&start=1&display=10&startDate=",days[i],"&endDate=",days[i],"&dnaSo=rel.dsc&page=",sep="")
 
  dt = read_html(url)
 
  result_num = dt %>% html_nodes(".result_num") %>% html_text()
 
  
  ret = tryCatch({
    result_num = strtoi(str_match(result_num,"\\/\\s*(\\d*)")[,2])  
  }, error = function(err){
    return("not found!")
    
  })
  
  if(ret =="not found!") next
  
  page_num = ceiling((result_num/10))
  
  cnt=0

  
  for( j in 1:page_num)
  {
    print(j)
    url = paste("http://news.naver.com/main/search/search.nhn?query=",query_str,"&st=news.all&q_enc=EUC-KR&r_enc=UTF-8&r_format=xml&rp=none&sm=title.basic&ic=all&so=rel.dsc&detail=1&pd=4&r_cluster2_start=1&r_cluster2_display=10&start=1&display=10&startDate=",days[i],"&endDate=",days[i],"&dnaSo=rel.dsc&page=",j,sep="")
    print(url)
    dt = read_html(url)
    
    lists = dt %>% html_nodes(".tit") %>% html_text()
    
    for (list in lists)
    {
      title_v = c(title_v,list) 
      date_v = c(date_v,as.character(days[i]))
     
    }
    
  }
  

}

result = data.frame(date_v,title_v)


# Year Split
result$date_v=str_split_fixed(result$date_v, "-",2)[,2]

# Date Count
b= result %>%
  group_by(date_v) %>%
  distinct(title_v) %>%
  summarise(merge=paste(title_v,collapse="<br>"),
            count=n())

b$merge=gsub("'","",b$merge)


g=ggplot(data=b,aes(x=date_v,y=count,group=1))+
  xlab("날짜") + ylab("건수") +
  geom_line(colour="red")+
  theme_bw()+
  geom_point_interactive(aes(tooltip=merge),size=0.5,alpha=0.5)+
  theme(axis.text.x = element_text(angle=70,hjust=1),text = element_text(size=8))

ggiraph(code=print(g),width=1,height=3)

