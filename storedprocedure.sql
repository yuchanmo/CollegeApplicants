DELIMITER $$
create procedure 'check_school' 
(in pname nvarchar(200),
 in pcapacity int,
 in pdistrict char(2),
 in pminscore int,
 in padjustratio float
)
begin
    if pcapacity < 1 then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Please enter value over 0 for Capacity'
    end if;

    if pdistrict not in ('A','B','C') then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Please enter only A or B or C for school district'
    end if;
end$$

DELIMITER ;

-- before insert
DELIMITER $$
CREATE TRIGGER `check_school_before_insert` BEFORE INSERT ON `parts`
FOR EACH ROW
BEGIN
in pname nvarchar(200),
 in pcapacity int,
 in pdistrict char(2),
 in pminscore int,
 in padjustratio float
    CALL check_school(new.cost,new.price);
END$$   
DELIMITER ; 
-- before update
DELIMITER $$
CREATE TRIGGER `parts_before_update` BEFORE UPDATE ON `parts`
FOR EACH ROW
BEGIN
    CALL check_parts(new.cost,new.price);
END$$   
DELIMITER ;



        