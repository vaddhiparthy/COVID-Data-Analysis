## STAT 6970 Master's Project: Analysis ##
#Beta regression modeling
install.packages("betareg")
library(betareg)
library(car)

#Loading and partitioning dataset
covid_census <- read.csv('census_wide_final.csv')
series_complete <- covid_census[, -2]
colnames(covid_census)

#Subset selection (domain knowledge/questions of interest)
series_all <- betareg(Series_Complete_Pop_Pct ~ ., data = series_complete[, -1])
summary(series_all)
vif(series_all)
#Starting selection based on signif coeff, and highest vif valued coeff
# % administered, 65+, BA+, poverty est
series_red <- betareg(Series_Complete_Pop_Pct ~ 
                         Admin.Distrib +
                         Proportion.65.and.older +
                         Proportion.BA.or.Higher +
                         Poverty.Estimate, data = series_complete[, -1])
summary(series_red)
#% administered, 65+, BA+
series_red2 <- betareg(Series_Complete_Pop_Pct ~ 
                         Admin.Distrib +
                         Proportion.65.and.older +
                         Proportion.BA.or.Higher, data = series_complete[, -1])
#% administered, 65+, <HS
series_red3 <- betareg(Series_Complete_Pop_Pct ~
                         Admin.Distrib +
                         Proportion.65.and.older +
                         Proportion.Less.than.HS, data = series_complete[, -1])
#% administered, 18-64, HS-AA
series_red4 <- betareg(Series_Complete_Pop_Pct ~
                         Admin.Distrib +
                         Proportion.between.18.and.64 +
                         Proportion.HS.through.AA, data = series_complete[, -1])
#% administered, 65+, HS-AA
series_red5 <- betareg(Series_Complete_Pop_Pct ~
                         Admin.Distrib +
                         Proportion.65.and.older +
                         Proportion.HS.through.AA, data = series_complete[, -1])
#% administered, <18, HS-AA
series_red6 <- betareg(Series_Complete_Pop_Pct ~
                         Admin.Distrib +
                         Proportion.under.18 +
                         Proportion.HS.through.AA, data = series_complete[, -1])
#Model selection based on LOWESET AIC
AIC(series_all, series_red, series_red2, series_red3, series_red4, series_red5, series_red6)
#Reduced model 5 (% admin, 65+, HS - AA) best model
vif(series_red5)
summary(series_red5)


#Repeat models for booster shot data
add_dose_all <- betareg(Additional_Doses_Vax_Pct ~ ., data = covid_census[, -1])
summary(add_dose_all)
vif(add_dose_all)
#series complete, % admin, 65+, BA+ pov est
add_red <- betareg(Additional_Doses_Vax_Pct ~
                       Series_Complete_Pop_Pct +
                       Admin.Distrib +
                       Proportion.65.and.older +
                       Proportion.BA.or.Higher +
                       Poverty.Estimate, data = covid_census[, -1])
summary(add_red)
#series complete, % admin, 65+, BA+
add_red2 <- betareg(Additional_Doses_Vax_Pct ~
                       Series_Complete_Pop_Pct +
                       Admin.Distrib +
                       Proportion.65.and.older +
                       Proportion.BA.or.Higher, data = covid_census[, -1])
summary(add_red2)
#series complete, 65+. BA+
add_red3 <- betareg(Additional_Doses_Vax_Pct ~
                      Series_Complete_Pop_Pct +
                      Proportion.65.and.older +
                      Proportion.BA.or.Higher, data = covid_census[, -1])
summary(add_red3)
#series complete 65+, <HS
add_red4 <-  betareg(Additional_Doses_Vax_Pct ~
                       Series_Complete_Pop_Pct +
                       Proportion.65.and.older +
                       Proportion.Less.than.HS, data = covid_census[, -1])
summary(add_red4)
#series complete, 18-64
add_red5 <-  betareg(Additional_Doses_Vax_Pct ~
                       Series_Complete_Pop_Pct +
                       Proportion.between.18.and.64 +
                       Proportion.HS.through.AA, data = covid_census[, -1])
summary(add_red5)
#series complete, 65+, HS-AA
add_red6 <-  betareg(Additional_Doses_Vax_Pct ~
                       Series_Complete_Pop_Pct +
                       Proportion.65.and.older +
                       Proportion.HS.through.AA, data = covid_census[, -1])
summary(add_red6)
#series complete <18, HS-AA
add_red7 <-  betareg(Additional_Doses_Vax_Pct ~
                       Series_Complete_Pop_Pct +
                       Proportion.under.18 +
                       Proportion.HS.through.AA, data = covid_census[, -1])
summary(add_red7)
#series complete, HS-AA
add_red8 <-  betareg(Additional_Doses_Vax_Pct ~
                       Series_Complete_Pop_Pct +
                       Proportion.HS.through.AA, data = covid_census[, -1])
summary(add_red8)
#Model selection based on LOWEST AIC
AIC(add_dose_all, add_red, add_red2, add_red3, add_red4, add_red5, add_red6,
    add_red7, add_red8)
#Reduced model 8 (series complete, HS - AA) best model
vif(add_red8)
summary(add_red8)


#Final models:
# Proporiton of completed vax series
summary(series_red5)
AIC(series_red5)

#Proportion with vax booster
summary(add_red8)
AIC(add_red8)



## Creating a best subset selection method ##
library(purrr)
library(tidyverse)

#expand.grid function for subset selection function
model.grid <- function(n){
  n.list <- rep(list(0:1), n)
  expand.grid(n.list)
}

#custom best subset selection function, sorting based on AIC
best.subset <- function(y , x.vars, data){
  length(x.vars) %>%
    model.grid %>%
    apply(1, function(x) which(x > 0, arr.ind =  TRUE)) %>%
    map(function(x) x.vars[x]) %>%
    .[2:dim(model.grid(length(x.vars)))[1]] %>%
    map(function(x) betareg(paste0(y, " ~ ", paste(x, collapse = "+")),
                            data = data)) %>%
    map(function(x) AIC(x)) %>%
    do.call(rbind, .) %>%
    cbind(model.grid(length(x.vars))[-1, ], .) %>%
    arrange(., .)
}

#Completed vaccine series
y <- names(series_complete[2])
x.vars <- names(series_complete[-c(1,2)])
best_complete <- best.subset(y, x.vars, data = series_complete[-1])
names(best_complete)[names(best_complete) == "."] <- 'AIC'
head(best_complete, 5)
x.vars
#summary of top model (*third best based on AIC)
vac_series_final <- betareg(Series_Complete_Pop_Pct ~ Admin.Distrib + Proportion.65.and.older +
          Proportion.Less.than.HS + Proportion.BA.or.Higher, data = series_complete[-1])
summary(vac_series_final)
AIC(vac_series_final)
vif(vac_series_final)
#model diagnostics
par(mfrow = c(3,2))
plot(vac_series_final, which = 1:5)
#getting odds ratio for coefficients
exp(vac_series_final$coefficients$mean)

#Vaccine plus booster
y <- names(covid_census[2])
x.vars <- names(covid_census[-c(1,2)])
best_plus1 <- best.subset(y, x.vars, data = covid_census[-1])
head(best_plus1, 5)
x.vars
#summary of top model (*second best based on AIC)
Vac_plus1_final <- betareg(Additional_Doses_Vax_Pct ~ Series_Complete_Pop_Pct +
      Proportion.Less.than.HS + Proportion.BA.or.Higher, data = covid_census[-1])
summary(Vac_plus1_final)
AIC(Vac_plus1_final)
vif(Vac_plus1_final)
#model diagnostics
par(mfrow = c(3,2))
plot(Vac_plus1_final, which = 1:5)
#getting odds ratio for coefficients
exp(Vac_plus1_final$coefficients$mean)
