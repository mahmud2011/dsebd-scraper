package cmd

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"strconv"
	"strings"
	"time"

	"github.com/gocolly/colly/v2"
	"github.com/spf13/cobra"

	"github.com/mahmud2011/dsebd-scraper/domain"
)

// dayendsummaryCmd represents the dayendsummary command
var dayendarchiveCmd = &cobra.Command{
	Use:   "dayendarchive",
	Short: "Scrape day end archive",
	Long:  `Scrape day end archive`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("dayendarchive called")

		c := colly.NewCollector()
		items := []domain.DayEndArchiveItem{}

		c.OnHTML("table.table.table-bordered.background-white.shares-table.fixedHeader tr", func(e *colly.HTMLElement) {
			if e.Index == 0 {
				return
			}

			item := domain.DayEndArchiveItem{}

			item.Date, _ = time.Parse("2006-01-02", e.ChildText("td:nth-of-type(2)"))
			item.TradingCode = strings.TrimSpace(e.ChildText("td:nth-of-type(3) a"))
			item.LastTradedPrice, _ = strconv.ParseFloat(strings.ReplaceAll(e.ChildText("td:nth-of-type(4)"), ",", ""), 64)
			item.High, _ = strconv.ParseFloat(strings.ReplaceAll(e.ChildText("td:nth-of-type(5)"), ",", ""), 64)
			item.Low, _ = strconv.ParseFloat(strings.ReplaceAll(e.ChildText("td:nth-of-type(6)"), ",", ""), 64)
			item.OpeningPrice, _ = strconv.ParseFloat(strings.ReplaceAll(e.ChildText("td:nth-of-type(7)"), ",", ""), 64)
			item.ClosingPrice, _ = strconv.ParseFloat(strings.ReplaceAll(e.ChildText("td:nth-of-type(8)"), ",", ""), 64)
			item.YesterdaysClosingPrice, _ = strconv.ParseFloat(strings.ReplaceAll(e.ChildText("td:nth-of-type(9)"), ",", ""), 64)
			item.Trade, _ = strconv.Atoi(strings.ReplaceAll(e.ChildText("td:nth-of-type(10)"), ",", ""))
			item.ValueMN, _ = strconv.ParseFloat(strings.ReplaceAll(e.ChildText("td:nth-of-type(11)"), ",", ""), 64)
			item.Volume, _ = strconv.Atoi(strings.ReplaceAll(e.ChildText("td:nth-of-type(12)"), ",", ""))

			items = append(items, item)
		})

		c.Visit("https://www.dsebd.org/day_end_archive.php?startDate=2021-01-01&endDate=2021-12-31&inst=All%20Instrument&archive=data")

		content, err := json.Marshal(items)
		if err != nil {
			fmt.Println(err)
		}
		err = ioutil.WriteFile("data.json", content, 0644)
		if err != nil {
			log.Fatal(err)
		}
	},
}

func init() {
	rootCmd.AddCommand(dayendarchiveCmd)
}
