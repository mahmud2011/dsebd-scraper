package domain

import (
	"time"
)

type DayEndArchiveItem struct {
	Date                   time.Time `json:"date"`
	TradingCode            string    `json:"trading_code"`
	LastTradedPrice        float64   `json:"last_traded_price"`
	High                   float64   `json:"high"`
	Low                    float64   `json:"low"`
	OpeningPrice           float64   `json:"opening_price"`
	ClosingPrice           float64   `json:"closing_price"`
	YesterdaysClosingPrice float64   `json:"yesterdays_closing_price"`
	Trade                  int       `json:"trade"`
	ValueMN                float64   `json:"value_mn"`
	Volume                 int       `json:"volume"`
}
