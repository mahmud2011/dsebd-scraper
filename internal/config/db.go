package config

import (
	"time"

	"github.com/spf13/viper"
)

var d *DBCfg

type DBCfg struct {
	Host            string
	Port            int
	User            string
	Pass            string
	Name            string
	ConnMaxLifetime time.Duration
	MaxIdleConn     int
	MaxOpenConn     int
	Debug           bool
}

func LoadDBCfg() {
	d = &DBCfg{
		Host:            viper.GetString("database.host"),
		Port:            viper.GetInt("database.port"),
		User:            viper.GetString("database.user"),
		Pass:            viper.GetString("database.pass"),
		Name:            viper.GetString("database.name"),
		ConnMaxLifetime: viper.GetDuration("database.conn_max_lifetime") * time.Second,
		MaxIdleConn:     viper.GetInt("database.max_idle_conn"),
		MaxOpenConn:     viper.GetInt("database.max_open_conn"),
		Debug:           viper.GetBool("database.debug"),
	}
}

func DB() *DBCfg {
	return d
}
