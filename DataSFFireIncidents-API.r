##################################################
## Project: Collect API data on fire incidents
## Author: Christopher Hench
##################################################

flatten_json <- function(df) {

    for (col in names(df)) {
        if (is.list(df[[col]])) {
            i <- 1
            for (row in df[[col]]) {

                df[[col]][i] <- paste(row, collapse = '; ')
                i <- i + 1
            }
            df[[col]] <- unlist(df[[col]])
        }
    }
return (df)
}

base_url <- 'https://data.sfgov.org/resource/wbb6-uh78.json?'

incident_date <- '2017-10-22T00:00:00.000'
incident_date <- URLencode(URL = incident_date, reserved = TRUE)

get_request <- paste0(base_url, "incident_date=", incident_date)
print(get_request)

response <- httr::GET(url = get_request)
response <- httr::content(x = response, as = "text")
response_df <- data.frame(jsonlite::fromJSON(txt = response, simplifyDataFrame = TRUE, flatten = TRUE))

flattened <- flatten_json(response_df)

write.csv(flattened, file='fire-incidents.csv')