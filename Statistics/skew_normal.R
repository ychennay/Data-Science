library(fGarch)
library(ggpl)
library(ggplot2)

MEAN <- c(5.4304, .6746)
STD <- c(33.97454, 25.1111)
SKEWNESS <- c(-2.6, -3.266)

medicare <- rsnorm(200000, MEAN[1], STD[1], SKEWNESS[1])
overall <- rsnorm(200000, MEAN[2], STD[2], SKEWNESS[2])

mean(medicare)
stdev(medicare)
median(medicare)

mean(overall)
stdev(overall)
median(overall)

dat <- data.frame(xx = c(medicare, overall),yy = c(rep("Medicare", 200000), rep("Overall",200000)))
write.csv(dat,'generated_samples.csv')

getwd()

ggplot(dat,aes(x=xx)) + 
  geom_histogram(data=subset(dat,yy == 'Medicare'), aes(y = (..count..)/sum(..count..)), fill = "red", alpha = 0.6, bins = 75) +
  geom_histogram(data=subset(dat,yy == 'Overall'), aes(y = (..count..)/sum(..count..)),col = "black", fill = "green", alpha = 0.2, bins = 75) + 
  xlab("% Margin") +
  xlim(c(-150,75)) +
  ylab('% of Respondents') +
  scale_fill_manual(name="group",values=c("red","darkgray"),labels=c("a","b")) +
  ggtitle("Fitted Distributions of Survey Responses") + 
  scale_y_continuous(labels = scales::percent)

mean(overall > medicare)

percentiles <- seq(from = .1, to = .9, by = .05)

quantile(medicare, percentiles) 
quantile(overall,percentiles)
