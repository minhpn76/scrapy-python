# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

class CronjobPipeline(object):

    
    def __init__(self):
        _engine = create_engine("mysql:///data.db")
        _connection = _engine.connect()
        _metadata = MetaData()
        _stack_items = Table("posts", _metadata,
                            Column("id", Integer, primary_key=True),
                            Column("job_id", Integer),
                            Column("job_title", String(50)),
                            Column("area1", String(50)),
                            Column("employment_type", String(50)),
                            Column("job_category", String(50)),
                            Column("salary_range", String(50)),
                            Column("posted_date", DateTime()),
                            Column("age", Text),
                            Column("requirements", Text),
                            Column("salary", Text),
                            Column("period", Text),
                            Column("working_hour", Text),
                            Column("location", Text),
                            Column("desc", Text),
                            Column("company_name", String(50)),
                            Column("company_website", String(50)),
                            Column("representative", String(50)),
                            Column("email", String(50)),
                            Column("tel", String(50)),
                            Column("fax", String(50)),
                            Column("pr", Text)
                    )
        _metadata.create_all(_engine)
        self.connection = _connection
        self.stack_items = _stack_items

    def process_item(self, item, spider):
        is_valid = True
        for data in item:
            if not data:
                is_valid = False
                raise DropItem("Missing %s!" % data)

        if is_valid:
            query = self.stack_items.insert().values(
                job_id=item["job_id"], job_title=item["job_title"],
                area1=item["area1"], employment_type=item["employment_type"],
                job_category=item["job_category"], salary_range=item["salary_range"],
                posted_date=item["posted_date"], age=item["age"],
                requirements=item["requirements"], working_hour=item["working_hour"],
                location=item["location"], desc=item["desc"],
                company_name=item["company_name"], company_website=item["company_website"],
                representative=item["representative"], email=item["email"],
                tel=item["tel"], fax=item["fax"], pr=item["pr"]
            )
            self.connection.execute(ins_query)

        return item
