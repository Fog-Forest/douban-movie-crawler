<?php
//处理演员信息类
class video_info{
	public $actor_list = array();
	public function actor($actor){
		$actor = str_replace("[", "", $actor);//删除多余的符号
		$actor = str_replace("]", "", $actor);//删除多余的符号
		$actor = str_replace("'", '"', $actor);//删除多余的符号
		preg_match_all('#(?<=name": ").*?(?=")#', $actor, $temp);
		$this->actor_list = implode('/ ',$temp[0]);
		return $this->actor_list;
	}
}
?>