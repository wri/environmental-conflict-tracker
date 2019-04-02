data <- read.csv("data/external/kenya-agroforestry.csv", header = F, col.names = c("date", "theme", "amt"))
library(tidyverse)
library(lubridate)
data$date <- ymd(data$date)
data$week <- floor_date(data$date, unit = "week")
grouped <- data %>% group_by(week, theme) %>% summarise(s = mean(amt))

baseline_data <- grouped[grepl("AGRO_FORESTRY", grouped$theme),]
baseline_data$norm <- (baseline_data$s/mean(baseline_data$s))
baseline_data <- baseline_data %>%
  complete(week = seq.Date(min(week), ymd('2018-12-23'), by="week"))
baseline_data <- baseline_data[!duplicated(baseline_data),]

total <- grouped %>% 
  group_by(theme) %>%
  mutate(norm = s/mean(s)) %>%
  complete(week = seq.Date(ymd("2017-01-01"), ymd("2018-12-23"), by = "week")) %>%
  mutate(diff = norm - baseline_data$norm)

total_sum <- total %>%
  group_by(theme) %>% 
  mutate(n = sum(!is.na(s))) %>%
  filter(n > 90) %>%
  summarise(cor = cor.test(s, baseline_data$s, na.rm=T)$estimate)

total_sum <- total_sum[total_sum$n > 100,]

plot_data <- total[grepl("WB_436_FORESTRY", total$theme),]

ggplot(data = plot_data, aes(x=week, y = diff))+
  geom_smooth(aes(color = theme), se = F)

