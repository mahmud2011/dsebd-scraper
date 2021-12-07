package conn

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/go-sql-driver/mysql" // mysql driver
	"gorm.io/driver/mysql"
	"gorm.io/gorm"

	"github.com/mahmud2011/dsebd-scraper/internal/config"
)

var d *DB

type DB struct {
	RawSQL *sql.DB
	GormDB *gorm.DB
}

func ConnectDB(cfg *config.DBCfg) error {
	dsn := fmt.Sprintf("%s:%s@tcp(%s:%d)/%s?charset=utf8mb4&parseTime=True",
		cfg.User,
		cfg.Pass,
		cfg.Host,
		cfg.Port,
		cfg.Name)

	db, err := sql.Open("mysql", dsn)
	if err != nil {
		return err
	}

	db.SetMaxIdleConns(cfg.MaxIdleConn)
	db.SetMaxOpenConns(cfg.MaxOpenConn)
	db.SetConnMaxLifetime(cfg.ConnMaxLifetime)

	if err := db.Ping(); err != nil {
		return err
	}

	gormDB, err := gorm.Open(mysql.New(
		mysql.Config{
			Conn: db,
		}), &gorm.Config{
		SkipDefaultTransaction: true,
	})
	if err != nil {
		return err
	}

	d = &DB{
		RawSQL: db,
		GormDB: gormDB,
	}

	log.Printf("Database\nConnMaxLifetime: %v\nMaxIdleConn: %v\nMaxOpenConn: %v\n",
		cfg.ConnMaxLifetime,
		cfg.MaxIdleConn,
		cfg.MaxOpenConn)

	return nil
}

func GetDB() *DB {
	return d
}
